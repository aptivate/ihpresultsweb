from collections import defaultdict
from django.views.generic.simple import direct_to_template
from models import Submission
from target import calc_agency_targets
from django.http import HttpResponse

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
            d["comments"] = "\n".join([comment for comment in comments if comment])
            d["key"] = "%s_%s" % (agency, indicator)
        
    extra_context["targets"] = targets

    return direct_to_template(request, template=template_name, extra_context=extra_context)

def agency_scorecard_csv(request):
    agencies = Submission.objects.all().values("agency").distinct()
    agencies = [el["agency"] for el in agencies]
    fields = "file|agency|profile|er1|r1|er2a|r2a|er2b|r2b|er2c|r2c|er3|r3|er4|r4|er5a|r5a|er5b|r5b|er5c|r5c|er6|r6|er7|r7|er8|r8|p1|p2|p3|p4|p5|p6|p7|np1|np2|np3|np4|np5|np6|np7".split("|")

    output = ",".join(fields)
    targets = {} 

    for agency in agencies:
        fields_dict = defaultdict(str, {})
        fields_dict["file"] = fields_dict["agency"] = agency
        
        targets[agency] = calc_agency_targets(agency)
        for indicator, d in targets[agency].items():
            old_comments = d["comments"]
            comments = []
            for question_number, country, comment in old_comments:
                comments.append("%s %s] %s" % (question_number, country, comment))
            d["comments"] = "\n".join([comment for comment in comments if comment])
            d["key"] = "%s_%s" % (agency, indicator)

        output += "\n"
        output += ",".join([value for value  

    return HttpResponse(output)
