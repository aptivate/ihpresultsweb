from django.views.generic.simple import direct_to_template
from models import Submission
from target import calc_agency_targets

def agency_scorecard(request, template_name="submissions/agency_scorecard.html", extra_context=None):
    extra_context = extra_context or {}
    agencies = Submission.objects.all().values("agency").distinct()
    agencies = [el["agency"] for el in agencies]

    targets = {} 
    for agency in agencies:
        targets[agency] = calc_agency_targets(agency)
        for indicator, d in targets[agency].items():
            old_comments = d["comments"]
            comments = []
            for question_number, country, comment in old_comments:
                comments.append("%s %s] %s" % (question_number, country, comment))
            d["comments"] = "\n".join(comments)
        
    extra_context["targets"] = targets

    return direct_to_template(request, template=template_name, extra_context=extra_context)
