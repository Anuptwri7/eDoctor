from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Response, CheckupSubmission
from doctors.models import Doctor

@login_required
def start_checkup_view(request):
    questions = Question.objects.all()

    if request.method == 'POST':

        submission = CheckupSubmission.objects.create(user=request.user)


        responses_list = []

        for question in questions:
            answer = request.POST.get(f'question_{question.id}')
            Response.objects.create(
                submission=submission,
                question=question,
                answer=answer
            )
            responses_list.append({
                'text': question.text,
                'answer': answer,
                'type': question.question_type
            })


        disease_points = {}

        ai_rules = {

            "blood pressure": {
                "Hypertension": lambda v: 2 if v > 140 else 0,
                "Low Blood Pressure": lambda v: 2 if v < 90 else 0,
            },
            "blood sugar": {
                "Diabetes / High Sugar": lambda v: 2 if v > 180 else 0,
                "Low Blood Sugar": lambda v: 2 if v < 70 else 0,
            },
            "temperature": {
                "Fever / Infection": lambda v: 2 if v > 38 else 0,
                "Hypothermia": lambda v: 2 if v < 36 else 0,
            },
            "heart rate": {
                "Tachycardia / Heart Issue": lambda v: 2 if v > 100 else 0,
                "Bradycardia / Heart Issue": lambda v: 2 if v < 60 else 0,
            },
            "weight": {
                "Obesity / Metabolic Issue": lambda v: 1 if v > 100 else 0,
                "Underweight / Malnutrition": lambda v: 1 if v < 40 else 0,
            },

            "do you have chest pain?": {
                "Heart Disease / Angina": lambda ans: 3 if ans.lower() == "yes" else 0,
            },
            "do you have joint pain?": {
                "Arthritis / Joint Issue": lambda ans: 2 if ans.lower() == "yes" else 0,
            },
            "do you have headache?": {
                "Migraine / Neurological Issue": lambda ans: 2 if ans.lower() == "yes" else 0,
            },
            "do you have fatigue?": {
                "General Fatigue / Anemia": lambda ans: 2 if ans.lower() == "yes" else 0,
            },
            "do you have dizziness?": {
                "Vertigo / Neurological Issue": lambda ans: 1 if ans.lower() == "yes" else 0,
            },
        }

        for r in responses_list:
            key = r['text'].lower()
            answer = r['answer']

            if r['type'] == 'NUM':
                try:
                    value = float(answer)
                except:
                    value = 0
                if key in ai_rules:
                    for disease, func in ai_rules[key].items():
                        disease_points[disease] = disease_points.get(disease, 0) + func(value)
            elif r['type'] == 'BOOL':
                if key in ai_rules:
                    for disease, func in ai_rules[key].items():
                        disease_points[disease] = disease_points.get(disease, 0) + func(answer)

        possible_diseases = [d for d, pts in disease_points.items() if pts > 0]

        disease_department_map = {
            "Heart Disease / Angina": "Cardiology",
            "Hypertension": "Cardiology",
            "Low Blood Pressure": "Cardiology",
            "Tachycardia / Heart Issue": "Cardiology",
            "Bradycardia / Heart Issue": "Cardiology",
            "Diabetes / High Sugar": "Endocrinology",
            "Low Blood Sugar": "Endocrinology",
            "Fever / Infection": "General Medicine",
            "Hypothermia": "General Medicine",
            "Obesity / Metabolic Issue": "Nutritionist",
            "Underweight / Malnutrition": "Nutritionist",
            "Arthritis / Joint Issue": "Orthopedics",
            "Migraine / Neurological Issue": "Neurology",
            "General Fatigue / Anemia": "Hematology",
            "Vertigo / Neurological Issue": "Neurology",
        }

        recommended_departments = set()
        for disease in possible_diseases:
            if disease in disease_department_map:
                recommended_departments.add(disease_department_map[disease])

        recommended_doctors = Doctor.objects.filter(department__name__in=recommended_departments)

        return render(request, 'checkup/results.html', {
            'responses': responses_list,
            'possible_diseases': possible_diseases or ["No specific disease detected."],
            'recommended_departments': list(recommended_departments) or ["N/A"],
            'recommended_doctors': recommended_doctors
        })


    return render(request, 'checkup/start_checkup.html', {'questions': questions})
@login_required
def checkup_list_view(request):

    current_user = request.user
    checkups = CheckupSubmission.objects.filter(user=current_user).order_by('-created_at')
    return render(request, "checkup/checkup_list.html", {"checkups": checkups})

@login_required
def checkup_detail_view(request, pk):
    current_user = request.user
    checkup = get_object_or_404(CheckupSubmission, pk=pk, user=current_user)
    responses = checkup.responses.select_related('question')
    return render(request, "checkup/checkup_detail.html", {
        "checkup": checkup,
        "responses": responses
    })

@login_required
def recheck_checkup_view(request, pk):
    checkup = get_object_or_404(CheckupSubmission, pk=pk, user=request.user)
    saved_responses = checkup.responses.select_related('question')


    responses_list = []
    for r in saved_responses:
        responses_list.append({
            "text": r.question.text,
            "answer": r.answer,
            "type": r.question.question_type
        })


    disease_points = {}

    ai_rules = {
        "blood pressure": {
            "Hypertension": lambda v: 2 if v > 140 else 0,
            "Low Blood Pressure": lambda v: 2 if v < 90 else 0,
        },
        "blood sugar": {
            "Diabetes / High Sugar": lambda v: 2 if v > 180 else 0,
            "Low Blood Sugar": lambda v: 2 if v < 70 else 0,
        },
        "temperature": {
            "Fever / Infection": lambda v: 2 if v > 38 else 0,
            "Hypothermia": lambda v: 2 if v < 36 else 0,
        },
        "heart rate": {
            "Tachycardia / Heart Issue": lambda v: 2 if v > 100 else 0,
            "Bradycardia / Heart Issue": lambda v: 2 if v < 60 else 0,
        },
        "weight": {
            "Obesity / Metabolic Issue": lambda v: 1 if v > 100 else 0,
            "Underweight / Malnutrition": lambda v: 1 if v < 40 else 0,
        },


        "do you have chest pain?": {
            "Heart Disease / Angina": lambda ans: 3 if ans.lower() == "yes" else 0,
        },
        "do you have joint pain?": {
            "Arthritis / Joint Issue": lambda ans: 2 if ans.lower() == "yes" else 0,
        },
        "do you have headache?": {
            "Migraine / Neurological Issue": lambda ans: 2 if ans.lower() == "yes" else 0,
        },
        "do you have fatigue?": {
            "General Fatigue / Anemia": lambda ans: 2 if ans.lower() == "yes" else 0,
        },
        "do you have dizziness?": {
            "Vertigo / Neurological Issue": lambda ans: 1 if ans.lower() == "yes" else 0,
        },
    }

    for r in responses_list:
        key = r["text"].lower()
        answer = r["answer"]

        if r["type"] == "NUM":
            try:
                value = float(answer)
            except:
                value = 0

            if key in ai_rules:
                for disease, func in ai_rules[key].items():
                    disease_points[disease] = disease_points.get(disease, 0) + func(value)

        elif r["type"] == "BOOL":
            if key in ai_rules:
                for disease, func in ai_rules[key].items():
                    disease_points[disease] = disease_points.get(disease, 0) + func(answer)


    possible_diseases = [d for d, pts in disease_points.items() if pts > 0]

    disease_department_map = {
        "Heart Disease / Angina": "Cardiology",
        "Hypertension": "Cardiology",
        "Low Blood Pressure": "Cardiology",
        "Tachycardia / Heart Issue": "Cardiology",
        "Bradycardia / Heart Issue": "Cardiology",
        "Diabetes / High Sugar": "Endocrinology",
        "Low Blood Sugar": "Endocrinology",
        "Fever / Infection": "General Medicine",
        "Hypothermia": "General Medicine",
        "Obesity / Metabolic Issue": "Nutritionist",
        "Underweight / Malnutrition": "Nutritionist",
        "Arthritis / Joint Issue": "Orthopedics",
        "Migraine / Neurological Issue": "Neurology",
        "General Fatigue / Anemia": "Hematology",
        "Vertigo / Neurological Issue": "Neurology",
    }

    recommended_departments = {
        disease_department_map[d] for d in possible_diseases if d in disease_department_map
    }

    recommended_doctors = Doctor.objects.filter(department__name__in=recommended_departments)

    return render(request, "checkup/results.html", {
        "responses": responses_list,
        "possible_diseases": possible_diseases or ["No specific disease detected."],
        "recommended_departments": list(recommended_departments) or ["N/A"],
        "recommended_doctors": recommended_doctors
    })
