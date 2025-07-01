from collections import defaultdict
from django.utils.dateformat import format as date_format
import json as pyjson
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HealthTestResult, LabReportUpload
from .forms import HealthTestResultForm, LabReportUploadForm, HealthTestResultUploadForm, PDFExtractForm
from core.models import TimelineEvent
from django.contrib import messages
import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from .openrouter_pdf import extract_health_data_from_pdf, extract_text_from_pdf, extract_health_data_from_text
import io

@login_required
def test_result_view(request):
    # Filtering
    filters = Q(user=request.user)
    test_name = request.GET.get('test_name', '').strip()
    test_date = request.GET.get('test_date', '').strip()
    result_value = request.GET.get('result_value', '').strip()
    unit = request.GET.get('unit', '').strip()
    flagged = request.GET.get('flagged', '').strip()
    order_by = request.GET.get('sort', '-test_date')

    if test_name:
        filters &= Q(test_name__icontains=test_name)
    if test_date:
        filters &= Q(test_date=test_date)
    if result_value:
        try:
            filters &= Q(result_value=float(result_value))
        except ValueError:
            pass
    if unit:
        filters &= Q(unit__icontains=unit)
    if flagged == 'true':
        filters &= Q(flagged=True)
    elif flagged == 'false':
        filters &= Q(flagged=False)

    # Sorting
    allowed_sorts = ['test_name', '-test_name', 'test_date', '-test_date', 'result_value', '-result_value', 'unit', '-unit', 'flagged', '-flagged']
    if order_by not in allowed_sorts:
        order_by = '-test_date'

    results_qs = HealthTestResult.objects.filter(filters).order_by(order_by)

    # Pagination
    paginator = Paginator(results_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # --- Chart Data Preparation ---
    all_results = HealthTestResult.objects.filter(user=request.user)
    chart_metrics = sorted(set(all_results.values_list('test_name', flat=True)))
    chart_data = {}
    grouped = defaultdict(list)
    for r in all_results:
        grouped[r.test_name].append(r)
    for metric, items in grouped.items():
        # Sort by date
        items_sorted = sorted(items, key=lambda x: x.test_date)
        dates = [date_format(x.test_date, 'Y-m-d') for x in items_sorted]
        values = [x.result_value for x in items_sorted]
        # Use the most common unit, or the first
        unit = items_sorted[0].unit if items_sorted else ''
        # Reference range: use the most common, or the first non-null
        min_vals = [x.reference_range_min for x in items_sorted if x.reference_range_min is not None]
        max_vals = [x.reference_range_max for x in items_sorted if x.reference_range_max is not None]
        min_val = min_vals[0] if min_vals else None
        max_val = max_vals[0] if max_vals else None
        chart_data[metric] = {
            'dates': dates,
            'values': values,
            'min': min_val,
            'max': max_val,
            'unit': unit,
        }
    chart_data_json = pyjson.dumps(chart_data)
    # --- End Chart Data Preparation ---

    form = HealthTestResultForm()
    if request.method == 'POST':
        form = HealthTestResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.user = request.user
            result.save()
            form.save_m2m()
            messages.success(request, "Test result added.")
            return redirect('health_data:health_test_results')
    return render(request, 'health_data/health_test_results.html', {
        'form': form,
        'results': page_obj,
        'page_obj': page_obj,
        'request': request,
        'order_by': order_by,
        'chart_metrics': chart_metrics,
        'chart_data_json': chart_data_json,
    })

@login_required
@require_POST
def delete_test_result(request, pk):
    result = HealthTestResult.objects.filter(user=request.user, pk=pk).first()
    if result:
        result.delete()
        messages.success(request, "Test result deleted.")
    return redirect('health_data:health_test_results')

@login_required
@require_POST
def delete_test_results_by_date(request):
    date = request.POST.get('test_date')
    if date:
        deleted, _ = HealthTestResult.objects.filter(user=request.user, test_date=date).delete()
        messages.success(request, f"Deleted {deleted} test result(s) for {date}.")
    return redirect('health_data:health_test_results')

@login_required
def edit_test_result(request, pk):
    result = HealthTestResult.objects.filter(user=request.user, pk=pk).first()
    if not result:
        return redirect('health_data:health_test_results')
    if request.method == 'POST':
        form = HealthTestResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, "Test result updated.")
            return redirect('health_data:health_test_results')
    else:
        form = HealthTestResultForm(instance=result)
    return render(request, 'health_data/health_test_form.html', {'form': form, 'edit': True, 'result': result})

@login_required
def bulk_rename_test_name(request):
    if request.method == 'POST':
        old_name = request.POST.get('old_name')
        new_name = request.POST.get('new_name')
        if old_name and new_name:
            updated = HealthTestResult.objects.filter(user=request.user, test_name=old_name).update(test_name=new_name)
            messages.success(request, f"Renamed {updated} test(s) from '{old_name}' to '{new_name}'.")
            return redirect('health_data:health_test_results')
    return render(request, 'health_data/bulk_rename_test_name.html')

@login_required
def lab_upload_view(request):
    if request.method == 'POST':
        form = LabReportUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            return redirect('health_data:lab_upload')
    else:
        form = LabReportUploadForm()
    uploads = LabReportUpload.objects.filter(user=request.user)
    return render(request, 'health_data/lab_upload.html', {'form': form, 'uploads': uploads})


@login_required
def health_test_create(request):
    if request.method == 'POST':
        form = HealthTestResultForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.user = request.user
            test.save()
            form.save_m2m()

            # Timeline integration
            TimelineEvent.objects.create(
                user=request.user,
                event_type="exam_result",
                summary=f"{test.test_name} = {test.result_value} {test.unit}",
                related_object=test,
                timestamp=test.test_date,
                title=f"{test.test_name} Result"
            )

            return redirect('health_data:health_test_results')
    else:
        form = HealthTestResultForm()
    return render(request, 'health_data/health_test_form.html', {'form': form})

@login_required
def health_test_json_upload(request):
    if request.method == 'POST':
        form = HealthTestResultUploadForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = request.FILES['json_file']
            try:
                data = json.load(json_file)
                results = data.get('results', [])

                success_count = 0
                failure_count = 0
                failed_entries = []
                flagged_summaries = []
                flagged_dates = set()

                for entry in results:
                    try:
                        test = HealthTestResult.objects.create(
                            user=request.user,
                            test_date=entry['test_date'],
                            test_name=entry['test_name'],
                            result_value=entry['result_value'],
                            unit=entry['unit'],
                            reference_range_min=entry.get('reference_range_min'),
                            reference_range_max=entry.get('reference_range_max'),
                            flagged=entry.get('flagged', False),
                            note=entry.get('note', '')
                        )
                        TimelineEvent.objects.create(
                            user=request.user,
                            event_type='exam_result',
                            summary=f"{test.test_name} = {test.result_value} {test.unit}",
                            related_object=test,
                            timestamp=test.test_date,
                            title=f"{test.test_name} Result"
                        )
                        if test.flagged:
                            flagged_summaries.append(f"{test.test_name}: {test.result_value} {test.unit}")
                            flagged_dates.add(str(test.test_date))
                        success_count += 1
                    except Exception as entry_error:
                        failure_count += 1
                        failed_entries.append(str(entry_error))

                # Add a timeline event summarizing flagged results if any
                if flagged_summaries:
                    TimelineEvent.objects.create(
                        user=request.user,
                        event_type='test_result',
                        summary="Flagged results: " + "; ".join(flagged_summaries),
                        timestamp=flagged_dates and min(flagged_dates) or None,
                        title="Flagged Test Results"
                    )

                if success_count:
                    messages.success(request, f"Successfully uploaded {success_count} result(s).")
                if failure_count:
                    messages.warning(request, f"{failure_count} result(s) failed to import. See console or logs for details.")
                    print("Failed entries:", failed_entries)
                if not success_count and not failure_count:
                    messages.error(request, "No results were uploaded. Please check your JSON file format.")
                return redirect('health_data:health_test_results')
            except json.JSONDecodeError:
                messages.error(request, "The uploaded file is not valid JSON.")
            except Exception as e:
                messages.error(request, f"Unexpected error: {e}")
        else:
            print('Form errors:', form.errors)
            print('POST:', request.POST)
            print('FILES:', request.FILES)
            messages.error(request, "Invalid form submission. Please select a valid JSON file.")
        return redirect('health_data:health_test_results')
    messages.error(request, "Invalid request method.")
    return redirect('health_data:health_test_results')

@login_required
def health_test_pdf_upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('pdf_file')
        if uploaded_file:
            # Extract health data from the uploaded PDF file
            extraction_results = extract_health_data_from_pdf(uploaded_file, request.user)
            
            # Process the extraction results (this will depend on your extraction logic)
            for result in extraction_results:
                # For example, create HealthTestResult objects from the extracted data
                HealthTestResult.objects.create(
                    user=request.user,
                    test_date=result['test_date'],
                    test_name=result['test_name'],
                    result_value=result['result_value'],
                    unit=result['unit'],
                    reference_range_min=result.get('reference_range_min'),
                    reference_range_max=result.get('reference_range_max'),
                    flagged=result.get('flagged', False),
                    note=result.get('note', '')
                )
            
            messages.success(request, "Health data extracted and test results created from PDF.")
            return redirect('health_data:health_test_results')
        else:
            messages.error(request, "No file was uploaded. Please select a PDF file to upload.")
    return render(request, 'health_data/health_test_pdf_upload.html', {})

@login_required
def extract_pdf_view(request):
    from .models import LabReportUpload
    extracted_results = None
    extraction_error = None
    truncation_warning = None
    created = 0
    extracted_text = None
    char_count = 0
    max_chars = 8000
    lab_upload_id = request.POST.get('lab_upload_id')
    lab_upload = None
    if lab_upload_id:
        try:
            lab_upload = LabReportUpload.objects.get(id=lab_upload_id, user=request.user)
        except LabReportUpload.DoesNotExist:
            extraction_error = 'Could not find uploaded file. Please re-upload.'
    # Always load extracted_results from session if present
    extracted_results = request.session.get('extracted_results')
    if request.method == 'POST':
        form = PDFExtractForm(request.POST, request.FILES)
        extracted_text = request.POST.get('extracted_text')
        char_count = len(extracted_text) if extracted_text else 0
        # If this is the first upload step
        if not lab_upload and form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            source = form.cleaned_data['source']
            lab_upload = LabReportUpload.objects.create(
                user=request.user,
                file=pdf_file,
                source=source or '',
                parsed=False
            )
            pdf_file.seek(0)
            pdf_bytes = pdf_file.read()
            pdf_io = io.BytesIO(pdf_bytes)
            extracted_text = extract_text_from_pdf(pdf_io)
            if not extracted_text or not extracted_text.strip():
                # Try OCR if no extractable text
                from .openrouter_pdf import extract_text_from_pdf_with_easyocr
                extracted_text = extract_text_from_pdf_with_easyocr(pdf_io)
                char_count = len(extracted_text)
                if not extracted_text or not extracted_text.strip():
                    extraction_error = 'No extractable text found in the uploaded PDF, even with OCR.'
            else:
                char_count = len(extracted_text)
            if char_count > max_chars:
                extraction_error = f'Extracted text exceeds maximum length of {max_chars} characters. Please truncate or edit the text.'
        elif lab_upload:
            pdf_file = lab_upload.file
            pdf_file.open('rb')
            pdf_bytes = pdf_file.read()
            pdf_io = io.BytesIO(pdf_bytes)
            pdf_file.close()
            if extracted_text is not None and 'edit_text' in request.POST:
                char_count = len(extracted_text)
                if char_count > max_chars and 'truncate_text' in request.POST:
                    extracted_text = extracted_text[:max_chars]
                    char_count = max_chars
                if 'send_to_llm' in request.POST or 'truncate_text' in request.POST:
                    try:
                        results, truncation_warning = extract_health_data_from_text(extracted_text)
                        extracted_results = results
                        request.session['extracted_results'] = extracted_results
                    except Exception as e:
                        extraction_error = str(e)
            elif 'confirm_save' in request.POST:
                # Save results to DB
                if not extracted_results:
                    extraction_error = 'No extracted results found. Please extract again.'
                else:
                    created = 0
                    for r in extracted_results:
                        try:
                            HealthTestResult.objects.create(
                                user=request.user,
                                test_date=r.get('test_date'),
                                test_name=r.get('test_name'),
                                result_value=r.get('result_value'),
                                unit=r.get('unit'),
                                reference_range_min=r.get('reference_range_min'),
                                reference_range_max=r.get('reference_range_max'),
                                flagged=r.get('flagged', False),
                                note=r.get('note', '')
                            )
                            created += 1
                        except Exception as e:
                            print('Failed to save result:', r, e)
                    messages.success(request, f"Saved {created} test result(s) to your records.")
                    if 'extracted_results' in request.session:
                        del request.session['extracted_results']
                    return redirect('health_data:health_test_results')
            else:
                extracted_text = extract_text_from_pdf(pdf_io)
                char_count = len(extracted_text)
    else:
        form = PDFExtractForm()
    return render(request, 'health_data/extract_pdf.html', {
        'form': form,
        'extracted_results': extracted_results,
        'extraction_error': extraction_error,
        'truncation_warning': truncation_warning,
        'created': created,
        'extracted_text': extracted_text,
        'char_count': char_count,
        'max_chars': max_chars,
        'lab_upload_id': lab_upload.id if lab_upload else '',
    })