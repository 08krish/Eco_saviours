from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ComplaintForm
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from datetime import datetime
import zoneinfo # Standard library in Python 3.9+

# def home_view(request):
#     success_message = None
    
#     if request.method == 'POST':
#         form = ComplaintForm(request.POST,request.FILES)
#         if form.is_valid():
#             # 1. Save the complaint to your Django database
#             complaint = form.save()
            
#             # 2. Craft the email content dynamically based on user input
#             email_subject = f"ECO-SAVIOUR ALERT: {complaint.get_category_display()} at {complaint.location}"
#             email_body = f"""
#             Dear Authority,

#             A civic complaint has been registered via the Eco-Saviour Amdavad Portal.

#             Citizen Details:
#             - Name: {complaint.name}
#             - Contact: {complaint.phone}
#             - Email: {complaint.email}

#             Grievance Details:
#             - Issue Category: {complaint.get_category_display()}
#             - Incident Location: {complaint.location}

#             Description of the Issue:
#             {complaint.description}

#             Please initiate the necessary protocols to address this matter.

#             Regards,
#             Eco-Saviour Automation Desk
#             """
            
#             # 3. Trigger the email send action
#             try:
#                 send_mail(
#                     subject=email_subject,
#                     message=email_body,
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     recipient_list=['abcx15572@gmail.com'], # Put your test email or a dummy AMC email here
#                     fail_silently=False,
#                 )
#                 success_message = "Your grievance has been successfully logged and dispatched to the AMC department!"
#                 form = ComplaintForm() # Resets the form layout after submission
#             except Exception as e:
#                 success_message = "Data logged locally, but email dispatch failed. Check terminal configurations."
#     else:
#         form = ComplaintForm()

#     return render(request, 'complaints/home.html', {
#         'form': form,
#         'success_message': success_message
#     })

import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from fpdf import FPDF
from .forms import ComplaintForm
from .models import Complaint # Make sure your model is imported

# 1. The main form view: Saves and redirects to the success screen
def home_view(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save()
            # Redirect to the success page and pass the fresh complaint ID in the URL
            return redirect('complaint_success', complaint_id=complaint.id)
    else:
        form = ComplaintForm()
        
    return render(request, 'complaints/home.html', {'form': form})


# 2. The Success Screen view
def complaint_success_view(request, complaint_id):
    return render(request, 'complaints/success.html', {'complaint_id': complaint_id})


# 3. The hidden download view: Triggers ONLY when the button is clicked
def download_pdf_view(request, complaint_id):
    try:
        complaint = Complaint.objects.get(id=complaint_id)
    except Complaint.DoesNotExist:
        raise Http404("Complaint not found")

    # Build the exact same FPDF layout you verified earlier
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    
    # --- Design Layout Banner ---
    pdf.set_fill_color(6, 78, 59)
    pdf.rect(0, 0, 210, 35, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", style="B", size=22)
    pdf.ln(5)
    pdf.cell(0, 10, "Eco-Saviour Amdavad", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 5, "Official Civic Grievance & Wildlife Rescue Acknowledgment", ln=True, align="C")
    pdf.ln(15)
    
    pdf.set_text_color(51, 65, 85)
    pdf.set_font("Arial", style="B", size=12)
    pdf.set_text_color(5, 150, 105)
    pdf.cell(0, 8, "GRIEVANCE METADATA", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(50, 8, "Filing Channel:", border="B")
    pdf.cell(0, 8, "Digital Citizen Portal Grid", border="B", ln=True)
    pdf.ln(8)

    pdf.set_font("Arial", style="B", size=12)
    pdf.set_text_color(5, 150, 105)
    pdf.cell(0, 8, "SUBMITTED CITIZEN DETAILS", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    fields = [
        ("Full Name:", complaint.name),
        ("Contact Email:", complaint.email),
        ("Description:", complaint.description),
    ]
    
    for label, value in fields:
        pdf.set_font("Arial", style="B", size=10)
        pdf.cell(40, 8, label, border="B")
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(150, 8, str(value), border="B", ln=True)
        pdf.ln(2)
    
    pdf.ln(10)

    if complaint.image and os.path.exists(complaint.image.path):
        try:
            pdf.set_font("Arial", style="B", size=12)
            pdf.set_text_color(5, 150, 105)
            pdf.cell(0, 8, "EVIDENCE ATTACHMENT", ln=True)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(6)
            pdf.image(complaint.image.path, x=15, w=100)
        except Exception:
            pass

    temp_filename = f"temp_receipt_{complaint.id}.pdf"
    pdf.output(temp_filename)
    
    with open(temp_filename, 'rb') as pdf_file:
        pdf_data = pdf_file.read()
    
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
    
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="EcoSaviour_Receipt_{complaint.id}.pdf"'
    return response

def helpline_view(request):
    return render(request, 'complaints/helpline.html')

def intro_view(request):
    return render(request, 'complaints/intro.html')



from datetime import datetime
import zoneinfo

from datetime import datetime
import zoneinfo

def helpline_directory_view(request):
    # Establish regional standard time zone alignment
    ist_zone = zoneinfo.ZoneInfo("Asia/Kolkata")
    current_hour = datetime.now(ist_zone).hour

    # Grouped data partition structure mapped perfectly for template consumption
    categories_data = [
        {
            "category_name": "🐾 Animal & Bird Rescue Helplines",
            "lines": [
                {"name": "Karuna Animal Ambulance", "phone": "1962", "start": 0, "end": 24, "address": "Emergency Mobile Veterinary Wing (Statewide Service)"},
                {"name": "AMC CNCD (Cattle Control)", "phone": "079-25352525", "start": 0, "end": 24, "address": "AMC Cattle Control Division, Danapapith, Ahmedabad"},
                {"name": "Jivdaya Charitable Trust (NGO)", "phone": "+91 99244 18184", "start": 8, "end": 19, "address": "Inside Ahmedabad Panjrapole, Ambawadi, Ahmedabad"},
                {"name": "Samvedna Bird & Animal Trust", "phone": "+91 70695 97373", "start": 0, "end": 24, "address": "Near Haridarshan Cross Road, Naroda, Ahmedabad"},
                {"name": "Animal Care Charitable Trust", "phone": "+91 99798 50999", "start": 8, "end": 20, "address": "Near Shreyas Railway Crossing, Paldi, Ahmedabad"},
                {"name": "Asha Foundation", "phone": "+91 98798 77281", "start": 9, "end": 18, "address": "Plot No. 232, Hathijan-Ramol Road, Hathijan"},
                {"name": "Bejuban Charitable Trust", "phone": "+91 70462 19000", "start": 0, "end": 24, "address": "Sarkhej-Gandhinagar Highway Hub, Ahmedabad"}
            ]
        },
        {
            "category_name": "🌲 Forest & Wildlife Conservation",
            "lines": [
                {"name": "Gujarat Forest Dept Core Line", "phone": "1926", "start": 0, "end": 24, "address": "Aranya Bhavan, Sector 10A, Gandhinagar"},
                {"name": "State Wildlife Automation Matrix", "phone": "+91 83200 02000", "start": 0, "end": 24, "address": "Digital WhatsApp Integration Grid"},
                {"name": "Aranya Bhavan Wildlife Wing", "phone": "079-23254125", "start": 0, "end": 24, "address": "Chief Wildlife Warden Desk, Gandhinagar"},
                {"name": "Van Chetna Kendra (Vastrapur)", "phone": "76000 09845", "start": 8, "end": 18, "address": "Opposite Vastrapur Lake, Ahmedabad"}
            ]
        },
        {
            "category_name": "💧 Water Logging & Pollution Grievance",
            "lines": [
                {"name": "AMC Central Grievance Line", "phone": "155303", "start": 0, "end": 24, "address": "Mahanagar Seva Sadan Central Control Room, Ahmedabad"},
                {"name": "GPCB Pollution Complaint Desk", "phone": "079-23232152", "start": 10, "end": 18, "address": "Paryavaran Bhavan, Sector 10-A, Gandhinagar"}
            ]
        },
        {
            "category_name": "♻️ E-Waste & Solid Waste Management",
            "lines": [
                {"name": "AMC Waste Collection Grid", "phone": "1800-233-1133", "start": 7, "end": 22, "address": "Solid Waste Management Dept, Danapapith"},
                {"name": "ECS E-Waste Recycling Center", "phone": "079-40400300", "start": 10, "end": 19, "address": "ECS House, Near Navrangpura Railway Crossing"}
            ]
        }
    ]

    # Calculate real-time available status metrics for each sub-array element
    for section in categories_data:
        for line in section["lines"]:
            if line["start"] == 0 and line["end"] == 24:
                line["is_open"] = True
                line["time_text"] = "24 / 7 Active"
            else:
                line["is_open"] = line["start"] <= current_hour < line["end"]
                start_ampm = f"{line['start']:02d}:00 AM" if line['start'] < 12 else f"{(line['start']-12 if line['start'] > 12 else 12):02d}:00 PM"
                end_ampm = f"{line['end']:02d}:00 AM" if line['end'] < 12 else f"{(line['end']-12 if line['end'] > 12 else 12):02d}:00 PM"
                line["time_text"] = f"{start_ampm} - {end_ampm}"

    # Return 'categories' to context so the template loops over grouped nodes explicitly
    return render(request, 'complaints/directory.html', {'categories': categories_data})


import json
from django.shortcuts import render
from .models import WasteLog
def smart_disposal_guide_view(request):
    guide_items = [
        # ========================================
        # BATTERIES & ELECTRONICS
        # ========================================
        {
            "item": "AA Lithium & Alkaline Batteries",
            "danger_level": "CRITICAL",
            "impact": "Leaches heavy mercury and lithium metals straight into soil beds, poisoning groundwater systems.",
            "action": "Wrap terminals in tape. Drop off exclusively at certified e-waste collections or electronic vendor desks.",
            "category": "E-Waste"
        },
        {
            "item": "Smartphones & Electronic Devices",
            "danger_level": "HIGH",
            "impact": "Contains lead, cadmium, and brominated flame retardants that contaminate soil and water sources for decades.",
            "action": "Factory reset devices, remove SIM cards, and donate to authorized e-waste recyclers or electronic repair shops.",
            "category": "E-Waste"
        },
        {
            "item": "Laptop & Computer Batteries",
            "danger_level": "CRITICAL",
            "impact": "Lithium-ion batteries can explode in landfills, releasing toxic fumes and heavy metals into the environment.",
            "action": "Return to manufacturer (many have take-back programs) or drop at certified e-waste collection centers.",
            "category": "E-Waste"
        },
        {
            "item": "Chargers & Power Cords",
            "danger_level": "LOW",
            "impact": "Copper and plastic components take 500+ years to decompose, releasing microplastics into the ecosystem.",
            "action": "Donate to electronics recycling drives or sell to scrap dealers who extract copper for reuse.",
            "category": "E-Waste"
        },
        {
            "item": "Printer Cartridges & Toner",
            "danger_level": "HIGH",
            "impact": "Toner dust contains carcinogenic compounds that contaminate air and water when improperly disposed.",
            "action": "Return to office supply stores (Staples, HP) for recycling programs. Refill and reuse when possible.",
            "category": "E-Waste"
        },

        # ========================================
        # PLASTICS & PACKAGING
        # ========================================
        {
            "item": "Single-Use Plastic Wrap / Packaging Bags",
            "danger_level": "HIGH",
            "impact": "Street cows and dogs ingest these while foraging; causes catastrophic, often fatal intestinal blockages.",
            "action": "Clean food residues, segregate into dry waste, or pass directly to AMC door-to-door collection routes.",
            "category": "Plastic Waste"
        },
        {
            "item": "Plastic Water Bottles",
            "danger_level": "HIGH",
            "impact": "Takes 450+ years to decompose. Microplastics enter food chain, harming marine life and human health.",
            "action": "Rinse, crush, and drop in blue (recyclable) bins. Better yet: switch to reusable steel/glass bottles.",
            "category": "Plastic Waste"
        },
        {
            "item": "Styrofoam / Thermocol Packaging",
            "danger_level": "MODERATE",
            "impact": "Breaks into toxic microplastics that animals mistake for food, causing starvation and death.",
            "action": "Reuse for packaging, crumble into fillers, or dispose in designated plastic waste collection.",
            "category": "Plastic Waste"
        },
        {
            "item": "Plastic Cutlery & Straws",
            "danger_level": "MODERATE",
            "impact": "Sharp edges injure animals when ingested. Microplastics accumulate in oceans and soil.",
            "action": "Avoid using altogether. If used, wash and recycle through plastic waste collection programs.",
            "category": "Plastic Waste"
        },

        # ========================================
        # MEDICAL & PHARMACEUTICAL
        # ========================================
        {
            "item": "Expired Medications & Pill Strips",
            "danger_level": "MODERATE",
            "impact": "Dissolves into municipal water infrastructure, mutating local aquatic life and bird reproductive health.",
            "action": "Take out of original packaging, mix with an unappealing substance (like coffee grounds), seal in a bag, and discard.",
            "category": "Medical Waste"
        },
        {
            "item": "Syringes & Needles",
            "danger_level": "CRITICAL",
            "impact": "Used needles carry bloodborne diseases and injure sanitation workers and stray animals.",
            "action": "NEVER throw in open bins. Use puncture-proof containers and drop at hospital/hazardous waste collection.",
            "category": "Medical Waste"
        },
        {
            "item": "Used Sanitary Pads & Diapers",
            "danger_level": "HIGH",
            "impact": "Contains plastics and chemicals that take 500+ years to decompose. Causes soil and water contamination.",
            "action": "Wrap securely in newspaper, tie in plastic bag, and drop in designated waste bins (not recyclable).",
            "category": "Medical Waste"
        },
        {
            "item": "Glass Medicine Bottles",
            "danger_level": "LOW",
            "impact": "Broken glass injures animals and sanitation workers. Can take 1 million years to degrade.",
            "action": "Rinse and drop in glass recycling bins. Remove plastic caps for separate recycling.",
            "category": "Medical Waste"
        },

        # ========================================
        # GLASS & METALS
        # ========================================
        {
            "item": "Broken Tubelights & CFL Bulbs",
            "danger_level": "CRITICAL",
            "impact": "Contains toxic mercury vapor. Shards cause deep paw lacerations and subsequent infections to urban stray animals.",
            "action": "Carefully wrap completely in thick newspaper or cardboard box casings before placing into separate hazardous handling tags.",
            "category": "Glass Waste"
        },
        {
            "item": "Glass Bottles & Jars",
            "danger_level": "LOW",
            "impact": "Takes 1 million years to decompose. Broken glass injures animals and contaminates soil.",
            "action": "Rinse thoroughly, remove lids, and drop in designated glass recycling bins or sell to scrap dealers.",
            "category": "Glass Waste"
        },
        {
            "item": "Aluminum Cans",
            "danger_level": "LOW",
            "impact": "Takes 200+ years to decompose. Mining for new aluminum is energy-intensive and pollutes air.",
            "action": "Crush and drop in recycling bins. Aluminum is 100% recyclable and saves 95% energy compared to new production.",
            "category": "Metals"
        },
        {
            "item": "Metal Scrap (Iron, Steel, Copper)",
            "danger_level": "LOW",
            "impact": "Rusts and leaches heavy metals into soil, affecting plant growth and groundwater quality.",
            "action": "Sell to kabadiwalas (scrap dealers) who recycle into new products. Segregate by metal type.",
            "category": "Metals"
        },

        # ========================================
        # ORGANIC & FOOD WASTE
        # ========================================
        {
            "item": "Food Waste & Kitchen Scraps",
            "danger_level": "MODERATE",
            "impact": "Attracts rodents and stray animals. Produces methane gas (25x more potent than CO2) in landfills.",
            "action": "Compost at home, use biogas plants, or drop in green (organic) waste collection bins daily.",
            "category": "Organic Waste"
        },
        {
            "item": "Cooking Oil & Grease",
            "danger_level": "HIGH",
            "impact": "Clogs drains, pollutes water bodies, and kills aquatic life. Creates fatbergs in sewage systems.",
            "action": "NEVER pour down drains. Collect in sealed containers and hand over to biodiesel recyclers.",
            "category": "Organic Waste"
        },
        {
            "item": "Garden & Yard Waste",
            "danger_level": "LOW",
            "impact": "Burning releases carbon emissions. In landfills, produces methane gas.",
            "action": "Compost into natural fertilizer. Use for mulching. Drop at urban garden waste collection points.",
            "category": "Organic Waste"
        },

        # ========================================
        # HAZARDOUS WASTE
        # ========================================
        {
            "item": "Pesticides & Insecticide Containers",
            "danger_level": "CRITICAL",
            "impact": "Toxic chemicals seep into groundwater, poisoning animals and birds that drink from contaminated sources.",
            "action": "Triple rinse empty containers, crush, and dispose only at government-designated hazardous waste sites.",
            "category": "Hazardous Waste"
        },
        {
            "item": "Paint & Chemical Thinners",
            "danger_level": "CRITICAL",
            "impact": "Contains VOCs (Volatile Organic Compounds) that pollute air and water. Toxic to wildlife.",
            "action": "NEVER pour down drains. Dry out completely (if small amount) and dispose as solid hazardous waste.",
            "category": "Hazardous Waste"
        },
        {
            "item": "Old Car Oil & Lubricants",
            "danger_level": "CRITICAL",
            "impact": "One liter of oil contaminates 1 million liters of water. Devastating to aquatic ecosystems.",
            "action": "Collect in sealed containers and hand over to authorized oil recycling centers or service stations.",
            "category": "Hazardous Waste"
        },

        # ========================================
        # OTHER WASTE
        # ========================================
        {
            "item": "Old Clothes & Textiles",
            "danger_level": "MODERATE",
            "impact": "Synthetic fabrics release microplastics. Cotton cultivation uses massive water resources.",
            "action": "Donate wearable clothes to NGOs. Recycle unwearable clothes into cleaning rags or upcycle into bags.",
            "category": "Textile Waste"
        },
        {
            "item": "Tobacco & Cigarette Butts",
            "danger_level": "HIGH",
            "impact": "Single butt contains 7000+ chemicals. Takes 10+ years to decompose. Animals ingest them frequently.",
            "action": "Dispose in designated bins. NEVER throw on streets. Use pocket ashtrays to collect butts.",
            "category": "Other Waste"
        },
        {
            "item": "Household Cleaners & Detergents",
            "danger_level": "HIGH",
            "impact": "Contains phosphates and bleach that contaminate water bodies and kill aquatic life.",
            "action": "Switch to eco-friendly alternatives. Dispose empty containers in plastic recycling. Never mix products.",
            "category": "Hazardous Waste"
        },
        {
            "item": "Construction & Demolition Debris",
            "danger_level": "HIGH",
            "impact": "Dust causes respiratory issues in animals and humans. Debris blocks drainage and water sources.",
            "action": "Hire authorized debris disposal services. Reuse materials like bricks, tiles, and wood in new construction.",
            "category": "Other Waste"
        },
        {
            "item": "Thermometers (Mercury)",
            "danger_level": "CRITICAL",
            "impact": "Mercury is a neurotoxin. One broken thermometer can contaminate a 20-acre lake.",
            "action": "Contact hazardous waste facility for safe disposal. NEVER throw in regular bins or drains.",
            "category": "Hazardous Waste"
        },
        {
            "item": "Aerosol Cans (Deodorants, Spray Paint)",
            "danger_level": "MODERATE",
            "impact": "Compressed gases contribute to ozone depletion and air pollution.",
            "action": "Empty completely by using contents. Drop in metal recycling bins. NEVER crush or burn.",
            "category": "Metals"
        }
    ]
    
    return render(request, 'complaints/disposal_guide.html', {'guide_items': guide_items})



# from django.shortcuts import render
# from .models import AnimalHospital

# def animal_hospital_map_view(request):
#     # This view now simply serves the interface.
#     # The search logic is handled by the browser for better UX.
#     return render(request, 'complaints/hospital_map.html')


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import requests
from math import radians, sin, cos, sqrt, atan2


# ================================================================
# MAIN VIEW - Animal Hospital Finder Page
# ================================================================
def animal_hospital_map_view(request):
    """
    View for the animal hospital finder page
    """
    context = {
        'page_title': 'Eco-Saviour Amdavad | Animal Hospital Finder',
        'default_lat': 23.0225,
        'default_lon': 72.5714,
        'default_city': 'Ahmedabad',
    }
    return render(request, 'complaints/hospital_map.html', context)


# ================================================================
# API - Search Veterinary Clinics
# ================================================================
@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def search_clinics_api(request):
    """
    API endpoint to search for veterinary clinics via Overpass API
    """
    # Handle preflight CORS request
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken"
        return response

    try:
        # Parse JSON body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)
        
        lat = data.get('lat')
        lon = data.get('lon')
        radius = data.get('radius', 5000)
        
        # Validate coordinates
        if lat is None or lon is None:
            return JsonResponse({
                'success': False,
                'error': 'Missing lat/lon parameters'
            }, status=400)
        
        # Validate coordinate ranges
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return JsonResponse({
                'success': False,
                'error': 'Invalid coordinates'
            }, status=400)
        
        # Try to fetch from Overpass API
        clinics = fetch_from_overpass(lat, lon, radius)
        
        # If no clinics found, use fallback
        if not clinics:
            clinics = get_fallback_clinics(lat, lon)
        
        return JsonResponse({
            'success': True,
            'clinics': clinics,
            'count': len(clinics),
            'source': 'overpass' if clinics and clinics[0].get('is_osm') else 'fallback'
        })
        
    except Exception as e:
        print(f"Error in search_clinics_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ================================================================
# API - Geocode Address
# ================================================================
@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def geocode_address_api(request):
    """
    API endpoint to geocode an address using Nominatim
    """
    # Handle preflight CORS request
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken"
        return response

    try:
        # Parse JSON body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)
        
        address = data.get('address')
        
        if not address or not address.strip():
            return JsonResponse({
                'success': False,
                'error': 'Missing address parameter'
            }, status=400)
        
        # Call Nominatim API
        nominatim_url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'q': address.strip(),
            'format': 'json',
            'limit': 1
        }
        
        response = requests.get(
            nominatim_url, 
            params=params, 
            headers={'User-Agent': 'Eco-Saviour App/1.0'},
            timeout=10
        )
        
        if response.status_code != 200:
            return JsonResponse({
                'success': False,
                'error': 'Geocoding service unavailable'
            }, status=500)
        
        data = response.json()
        
        if not data or len(data) == 0:
            return JsonResponse({
                'success': False,
                'error': 'Address not found'
            }, status=404)
        
        return JsonResponse({
            'success': True,
            'lat': float(data[0]['lat']),
            'lon': float(data[0]['lon']),
            'display_name': data[0]['display_name']
        })
        
    except requests.exceptions.Timeout:
        return JsonResponse({
            'success': False,
            'error': 'Geocoding service timeout'
        }, status=504)
    except Exception as e:
        print(f"Error in geocode_address_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ================================================================
# HELPER FUNCTIONS
# ================================================================
def fetch_from_overpass(lat, lon, radius):
    """
    Fetch veterinary clinics from Overpass API
    """
    try:
        overpass_url = 'https://overpass-api.de/api/interpreter'
        query = f"""
            [out:json];
            (
                node["amenity"="veterinary"](around:{radius},{lat},{lon});
                way["amenity"="veterinary"](around:{radius},{lat},{lon});
                relation["amenity"="veterinary"](around:{radius},{lat},{lon});
            );
            out center;
        """
        
        response = requests.post(
            overpass_url, 
            data=query, 
            timeout=15,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if response.status_code != 200:
            return []
        
        overpass_data = response.json()
        clinics = []
        
        for element in overpass_data.get('elements', []):
            # Get coordinates
            if 'center' in element:
                lat_val = element['center']['lat']
                lon_val = element['center']['lon']
            else:
                lat_val = element.get('lat')
                lon_val = element.get('lon')
            
            if not lat_val or not lon_val:
                continue
            
            tags = element.get('tags', {})
            clinics.append({
                'id': element.get('id'),
                'name': tags.get('name', 'Unnamed Clinic'),
                'lat': float(lat_val),
                'lon': float(lon_val),
                'phone': tags.get('phone', ''),
                'website': tags.get('website', ''),
                'hours': tags.get('opening_hours', 'Hours not specified'),
                'address': tags.get('addr:full', '') or tags.get('addr:street', ''),
                'is_osm': True
            })
        
        # Calculate distances
        for clinic in clinics:
            clinic['distance'] = haversine_distance(lat, lon, clinic['lat'], clinic['lon'])
        
        # Sort by distance
        clinics.sort(key=lambda x: x['distance'])
        
        return clinics
        
    except Exception as e:
        print(f"Overpass API error: {str(e)}")
        return []


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two points in kilometers
    """
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))

# Add this function to your views.py if not already present

def get_fallback_clinics(lat, lon):
    """
    Fallback clinic data for Ahmedabad - Updated with more accurate coordinates
    """
    fallback_data = [
        {"name": "Karuna Animal Ambulance", "lat": 23.0030, "lon": 72.5480, "phone": "1962", "hours": "24/7 Active", "address": "Ahmedabad"},
        {"name": "Jivdaya Charitable Trust", "lat": 23.0330, "lon": 72.5450, "phone": "+919924418181", "hours": "08:00 - 19:00", "address": "Near Jain Temple, Ahmedabad"},
        {"name": "Animal Care Charitable Trust", "lat": 23.0110, "lon": 72.5530, "phone": "+919979850999", "hours": "Office Hours", "address": "Maninagar, Ahmedabad"},
        {"name": "Bejuban Charitable Trust", "lat": 23.0800, "lon": 72.6360, "phone": "+917046219000", "hours": "Office Hours", "address": "Vastral, Ahmedabad"},
        {"name": "Samvedna Bird & Animal Trust", "lat": 23.0780, "lon": 72.6350, "phone": "+917069597373", "hours": "09:00-20:00", "address": "Vastral, Ahmedabad"},
        {"name": "Aranya Bhavan Wildlife Wing", "lat": 23.1890, "lon": 72.6310, "phone": "07923254125", "hours": "10:30-18:00", "address": "Gandhinagar Highway"},
        {"name": "Van Chetna Kendra", "lat": 23.0370, "lon": 72.5280, "phone": "7600009845", "hours": "10:00-18:00", "address": "Vastrapur, Ahmedabad"},
        {"name": "Ashram Road Vet Center", "lat": 23.0330, "lon": 72.5710, "phone": "+919825012345", "hours": "09:00-21:00", "address": "Ashram Road, Ahmedabad"},
        {"name": "Maninagar Animal Clinic", "lat": 23.0070, "lon": 72.6070, "phone": "+919825067890", "hours": "10:00-20:00", "address": "Maninagar, Ahmedabad"},
        {"name": "Vastrapur Pet Care", "lat": 23.0370, "lon": 72.5280, "phone": "+919825055555", "hours": "08:00-22:00", "address": "Vastrapur, Ahmedabad"},
        {"name": "Satellite Pet Hospital", "lat": 23.0250, "lon": 72.5180, "phone": "+919825044444", "hours": "24/7 Always Open", "address": "Satellite, Ahmedabad"}
    ]
    
    # Calculate distances
    for clinic in fallback_data:
        clinic['distance'] = haversine_distance(lat, lon, clinic['lat'], clinic['lon'])
        clinic['is_osm'] = False
    
    return sorted(fallback_data, key=lambda x: x['distance'])


def problems_solutions_view(request):
    """
    View for the Problems & Solutions page
    """
    context = {
        'page_title': 'Eco-Saviour Amdavad | Environmental Problems & Solutions',
    }
    return render(request, 'complaints/problem_solution.html', context)

def surveys_view(request):
    """
    View for the Surveys page
    """
    context = {
        'page_title': 'Eco-Saviour Amdavad | Our Surveys',
    }
    return render(request, 'complaints/surveys.html', context)