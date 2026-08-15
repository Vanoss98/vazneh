from django.db import migrations


def populate_english_content(apps, schema_editor):
    ProductType = apps.get_model("main", "ProductType")
    Product = apps.get_model("main", "Product")
    ProductCapacity = apps.get_model("main", "ProductCapacity")
    ProductSize = apps.get_model("main", "ProductSize")
    ProductFeature = apps.get_model("main", "ProductFeature")
    Project = apps.get_model("main", "Project")
    ProjectFeature = apps.get_model("main", "ProjectFeature")
    Representative = apps.get_model("main", "Representative")
    Service = apps.get_model("main", "Service")
    ServiceItem = apps.get_model("main", "ServiceItem")
    BlogPost = apps.get_model("main", "BlogPost")

    product_type_translations = {
        "جرثقیل-سقفی-تک-پل": "Single-Girder Overhead Crane",
        "جرثقیل-سقفی-دو-پل": "Double-Girder Overhead Crane",
    }
    for slug, title_en in product_type_translations.items():
        ProductType.objects.filter(slug=slug).update(title_en=title_en)

    product_translations = {
        "جرثقیل-سقفی-تک-پل-نمونه": {
            "title_en": "Single-Girder Overhead Crane",
            "subtitle_en": "A lightweight, economical, and dependable solution",
            "short_description_en": (
                "Vazneh single-girder overhead cranes are designed for safe load "
                "handling in industrial halls and can be customized for each project."
            ),
            "detailed_description_en": (
                "Each crane is engineered around the hall dimensions, required "
                "capacity, and operating conditions. Its compact structure, easy "
                "maintenance access, and flexible controls make it an economical "
                "choice for production lines and industrial warehouses."
            ),
        },
        "جرثقیل-سقفی-دو-پل-نمونه": {
            "title_en": "Double-Girder Overhead Crane",
            "subtitle_en": "More power for demanding industrial projects",
            "short_description_en": (
                "Vazneh double-girder overhead cranes serve high capacities and wide "
                "spans, with support for project-specific equipment."
            ),
            "detailed_description_en": (
                "The double-girder model is designed for heavy-duty cycles, high "
                "capacities, and wide spans. Every unit follows industrial standards "
                "and can include a cabin, remote control, and dedicated safety systems."
            ),
        },
    }
    for slug, values in product_translations.items():
        Product.objects.filter(slug=slug).update(**values)

    option_translations = {
        "۲ تا ۵ تن": "2 to 5 tons",
        "۵ تا ۱۵ تن": "5 to 15 tons",
        "۱۰ تا ۳۰ تن": "10 to 30 tons",
        "بیش از ۳۰ تن": "More than 30 tons",
        "سایز ۱": "Size 1",
        "سایز ۲": "Size 2",
        "سایز ۳": "Size 3",
        "سایز ۴": "Size 4",
    }
    for title, title_en in option_translations.items():
        ProductCapacity.objects.filter(title=title).update(title_en=title_en)
        ProductSize.objects.filter(title=title).update(title_en=title_en)

    feature_translations = {
        "طراحی کم‌حجم": "Compact design",
        "نصب سریع": "Fast installation",
        "مصرف انرژی بهینه": "Optimized energy use",
        "امکان سفارشی‌سازی": "Customizable configuration",
        "مناسب صنایع سنگین": "Built for heavy industry",
        "کنترل دقیق بار": "Precise load control",
    }
    for title, title_en in feature_translations.items():
        ProductFeature.objects.filter(title=title).update(title_en=title_en)

    project_translations = {
        "پروژه-فولاد-مبارکه-اصفهان": {
            "title_en": "Mobarakeh Steel Project, Isfahan",
            "subtitle_en": "Production-line overhead crane design and installation",
            "description_en": (
                "The overhead crane for this facility was designed, manufactured, "
                "and installed for a demanding duty cycle and strict production-line "
                "safety requirements. Vazneh completed all engineering and "
                "commissioning stages."
            ),
            "location_en": "Mobarakeh Steel Complex, Isfahan",
        },
        "پروژه-سالن-صنعتی-تهران": {
            "title_en": "Tehran Industrial Hall Project",
            "subtitle_en": "Material-handling system supply and installation",
            "description_en": (
                "A complete material-handling system was designed for this hall, from "
                "site measurements through installation and final handover. The "
                "solution provides a safer workspace and faster production access."
            ),
            "location_en": "Shamsabad Industrial City, Tehran",
        },
    }
    for slug, values in project_translations.items():
        Project.objects.filter(slug=slug).update(**values)

    project_feature_translations = {
        "ظرفیت باربری بالا": "High load capacity",
        "کنترل از راه دور": "Remote control",
        "چرخه کاری سنگین": "Heavy-duty cycle",
        "طراحی اختصاصی": "Purpose-built design",
        "نصب و راه‌اندازی": "Installation and commissioning",
        "پشتیبانی فنی": "Technical support",
    }
    for title, title_en in project_feature_translations.items():
        ProjectFeature.objects.filter(title=title).update(title_en=title_en)

    representative_translations = {
        "مهندس علی رضایی": (
            "Ali Rezaei",
            "Tehran",
            "Vozara Street, Samoot Building, 2nd Floor, Tehran",
        ),
        "مهندس مهدی کاظمی": (
            "Mehdi Kazemi",
            "Isfahan",
            "Chaharbagh-e Bala Street, Sepehr Office Complex, Isfahan",
        ),
        "مهندس سارا احمدی": (
            "Sara Ahmadi",
            "Shiraz",
            "Chamran Boulevard, Pars Building, Shiraz",
        ),
        "مهندس امیر موسوی": (
            "Amir Mousavi",
            "Rasht",
            "Gilan Boulevard, Golsar Commercial Complex, Rasht",
        ),
        "مهندس رضا اکبری": (
            "Reza Akbari",
            "Tabriz",
            "Valiasr, Shahriar Street, Tabriz",
        ),
        "مهندس نازنین کریمی": (
            "Nazanin Karimi",
            "Kerman",
            "Jomhouri Eslami Boulevard, Baran Commercial Tower, Kerman",
        ),
    }
    for name, (name_en, city_en, address_en) in representative_translations.items():
        Representative.objects.filter(name=name).update(
            name_en=name_en,
            city_en=city_en,
            address_en=address_en,
        )

    service_translations = {
        "maintenance": {
            "title_en": "Repair and Maintenance",
            "subtitle_en": "Keep equipment safe with scheduled specialist service",
            "short_description_en": (
                "Vazneh's service team prevents unplanned lifting-equipment downtime "
                "through scheduled inspections, preventive repairs, and rapid response."
            ),
            "detailed_description_en": (
                "Every maintenance program is based on equipment type, duty level, "
                "environment, and safety requirements. Clear technical reports, parts "
                "recommendations, and service records help control cost and downtime."
            ),
        },
        "lifting-equipment": {
            "title_en": "Lifting Equipment Manufacturing",
            "subtitle_en": "Load-handling equipment engineered for real production needs",
            "short_description_en": (
                "Design and manufacture of lifting devices, load-handling accessories, "
                "and custom solutions that improve industrial safety and throughput."
            ),
            "detailed_description_en": (
                "From load analysis to material selection and final testing, Vazneh "
                "equipment is engineered around capacity, load geometry, and operating "
                "conditions for a reliable and ergonomic result."
            ),
        },
        "industrial-structures": {
            "title_en": "Industrial Structures",
            "subtitle_en": "Precision structures for lasting load-bearing performance",
            "short_description_en": (
                "Vazneh designs, manufactures, and quality-checks steel structures for "
                "crane runways, industrial halls, and special projects."
            ),
            "detailed_description_en": (
                "Structures are designed for working loads, site conditions, and "
                "installation requirements. Dimensional, connection, and coating "
                "quality controls support faster installation and a longer service life."
            ),
        },
        "spare-parts": {
            "title_en": "Accessories and Spare Parts",
            "subtitle_en": "Dependable parts that protect quality, safety, and uptime",
            "short_description_en": (
                "Supply of mechanical and electrical spare parts, safety equipment, "
                "and crane accessories with expert selection support."
            ),
            "detailed_description_en": (
                "An incompatible part can reduce both safety and equipment life. "
                "Vazneh specialists match the device model, capacity, and duty "
                "conditions, with installation and adjustment available when needed."
            ),
        },
        "installation": {
            "title_en": "Transport and Installation",
            "subtitle_en": "Safe delivery from the Vazneh factory to commissioning",
            "short_description_en": (
                "Coordinated transport, assembly, installation, adjustment, and "
                "commissioning for heavy equipment at the customer's site."
            ),
            "detailed_description_en": (
                "Before delivery, the team reviews transport routes, access points, "
                "assembly areas, and safety requirements. Mechanical and electrical "
                "installation is followed by motion and performance testing."
            ),
        },
        "consulting": {
            "title_en": "Consulting",
            "subtitle_en": "Better engineering decisions before investment and execution",
            "short_description_en": (
                "Specialist advice on crane type, capacity, layout, process "
                "optimization, expansion, and modernization."
            ),
            "detailed_description_en": (
                "Vazneh consulting starts with material flow and operating needs. "
                "Deliverables can include technical recommendations, option comparisons, "
                "initial layouts, and an execution roadmap that reduces future risk."
            ),
        },
    }
    for slug, values in service_translations.items():
        Service.objects.filter(slug=slug).update(**values)

    service_item_translations = {
        "maintenance": {
            ("benefit", 1): ("Complete technical inspection", "Checks the structure, drives, brakes, ropes, and safety devices."),
            ("benefit", 2): ("Reduced production downtime", "Detects wear before it develops into a serious failure."),
            ("benefit", 3): ("Specialist support", "Direct access to experts in Vazneh cranes and industrial equipment."),
            ("process", 1): ("Site visit and assessment", "Reviews the current condition and records operating needs."),
            ("process", 2): ("Service plan", "Defines priorities, timing, and required parts."),
            ("process", 3): ("Execution and report", "Completes repairs, testing, and the final technical report."),
        },
        "lifting-equipment": {
            ("benefit", 1): ("Purpose-built design", "Matches the equipment to load dimensions, weight, and attachment points."),
            ("benefit", 2): ("Controlled manufacturing", "Controls materials, welding, and build quality throughout production."),
            ("benefit", 3): ("Load testing", "Verifies performance and safety before final delivery."),
            ("process", 1): ("Define the requirement", "Collects load data and workspace limitations."),
            ("process", 2): ("Design and approval", "Prepares the engineering design with the operations team."),
            ("process", 3): ("Manufacture and delivery", "Builds, tests, and supplies safe-use documentation."),
        },
        "industrial-structures": {
            ("benefit", 1): ("Engineering calculations", "Designs around real loads and installation-site conditions."),
            ("benefit", 2): ("Dimensional accuracy", "Builds to drawings to minimize site corrections."),
            ("benefit", 3): ("Quality control", "Inspects connections, welds, and final coating."),
            ("process", 1): ("Site survey", "Measures the site and reviews existing structural constraints."),
            ("process", 2): ("Execution design", "Prepares shop drawings and connection details."),
            ("process", 3): ("Manufacture and preparation", "Produces, checks, and prepares components for transport."),
        },
        "spare-parts": {
            ("benefit", 1): ("Accurate technical selection", "Matches part specifications to the equipment model and capacity."),
            ("benefit", 2): ("Broad product range", "Supplies mechanical, electrical, and safety components."),
            ("benefit", 3): ("Installation available", "Provides installation, adjustment, and testing by Vazneh technicians."),
            ("process", 1): ("Part identification", "Reviews the code, photo, or current equipment specifications."),
            ("process", 2): ("Technical proposal", "Recommends the right option and confirms supply conditions."),
            ("process", 3): ("Delivery and support", "Ships the part with installation guidance or field service."),
        },
        "installation": {
            ("benefit", 1): ("Integrated planning", "Coordinates transport and installation to reduce site disruption."),
            ("benefit", 2): ("Specialist field team", "Uses technicians trained in equipment and safety standards."),
            ("benefit", 3): ("Complete commissioning", "Adjusts, tests, and introduces the equipment to operators."),
            ("process", 1): ("Site preparation", "Checks the route, unloading area, and installation prerequisites."),
            ("process", 2): ("Transport and assembly", "Moves and assembles equipment under the execution plan."),
            ("process", 3): ("Commissioning", "Performs no-load and load tests before handover."),
        },
        "consulting": {
            ("benefit", 1): ("Independent engineering view", "Assesses the real need and project constraints."),
            ("benefit", 2): ("Solution comparison", "Compares cost, capacity, and expandability."),
            ("benefit", 3): ("Lower execution risk", "Identifies challenges before manufacturing and installation."),
            ("process", 1): ("Understand the need", "Runs a technical meeting and visits the process or project site."),
            ("process", 2): ("Analyze options", "Reviews capacity, layout, and execution requirements."),
            ("process", 3): ("Provide the roadmap", "Delivers the technical proposal and next project steps."),
        },
    }
    for slug, item_map in service_item_translations.items():
        service = Service.objects.filter(slug=slug).first()
        if not service:
            continue
        for (kind, position), (title_en, description_en) in item_map.items():
            ServiceItem.objects.filter(
                service_id=service.pk,
                kind=kind,
                position=position,
            ).update(title_en=title_en, description_en=description_en)

    blog_translations = {
        "choosing-workshop-crane": {
            "title_en": "How Do You Choose the Right Crane for a Workshop?",
            "excerpt_en": "A guide to matching crane capacity, span, and type to the workshop's real workflow.",
            "body_en": """
                <p>Choosing a crane is not only about rated capacity. The load path, duty cycles, available lifting height, and structural limitations all shape the final decision.</p>
                <h2>Start with the workflow</h2>
                <p>Before comparing models, record the load type, typical and maximum weight, pickup points, and destination. This information defines the required travel range and speed.</p>
                <blockquote>The right choice begins with a precise understanding of the process, not simply the highest capacity.</blockquote>
                <h2>Three deciding factors</h2>
                <ul><li>Safe capacity and duty class</li><li>Span, lifting height, and available clearance</li><li>Future service access and parts availability</li></ul>
                <p>Finally, a technical team should inspect the hall structure and power supply so the proposed solution is both safe and economical.</p>
            """,
        },
        "preventive-crane-maintenance": {
            "title_en": "Which Costs Does Preventive Crane Maintenance Reduce?",
            "excerpt_en": "Why a regular inspection plan reduces production stops and expensive failures.",
            "body_en": """
                <p>Many sudden failures begin with small signs: unusual noise, a warmer motor, or a change in brake behavior.</p>
                <h2>What does a periodic inspection reveal?</h2>
                <p>Checking the wire rope, hook, brakes, wheels, and electrical panel helps the maintenance team identify wear before it causes a serious shutdown.</p>
                <ol><li>Record the equipment baseline</li><li>Set service intervals for the actual duty level</li><li>Document results and corrective action</li></ol>
            """,
        },
        "safe-load-handling": {
            "title_en": "Principles of Safe Load Handling in Industry",
            "excerpt_en": "Practical principles that reduce risk while rigging, lifting, and moving heavy loads.",
            "body_en": """
                <p>Safe load handling depends on a coordinated operator, sound equipment, and clear instructions. Never move a suspended load without first evaluating its route.</p>
                <h2>Before lifting</h2>
                <ul><li>Identify the load weight and center of gravity.</li><li>Select the correct sling and attachments.</li><li>Clear people and obstacles from the travel path.</li></ul>
                <p>A low-height test lift is the final check before the main movement begins.</p>
            """,
        },
        "single-vs-double-girder": {
            "title_en": "Single or Double Girder: Which Crane Is Better?",
            "excerpt_en": "A comparison of the uses, capacities, and limitations of two common overhead crane structures.",
            "body_en": """
                <p>A single-girder crane is usually a lighter solution for moderate capacities and spans, while a double-girder model supports higher capacities and better hook height.</p>
                <h2>The comparison must be project-specific</h2>
                <p>Dead load, usable height, duty class, and maintenance costs should be considered together. A lower purchase price is not always the most economical choice over the equipment's life.</p>
            """,
        },
        "crane-modernization-signs": {
            "title_en": "When Does a Crane Need Modernization?",
            "excerpt_en": "Signs that isolated repairs are no longer enough and the equipment needs redesign.",
            "body_en": """
                <p>Repeated failures, unavailable compatible parts, and changing production needs are leading reasons to consider modernization.</p>
                <h2>Modernization is more than replacing a part</h2>
                <p>A sound project evaluates the structure, drives, electrical controls, and safety equipment as one integrated system.</p>
            """,
        },
        "lifting-equipment-inspection": {
            "title_en": "Lifting Equipment Inspection Checklist",
            "excerpt_en": "Key checks for slings, shackles, hooks, and accessories before use.",
            "body_en": """
                <p>A visual check before each shift complements specialist periodic inspections and can reveal obvious damage before an incident occurs.</p>
                <h2>Items that must not be ignored</h2>
                <ul><li>Deformation, cracks, or corrosion</li><li>A readable capacity plate</li><li>Sound hook latches and connections</li><li>Recording and removing faulty equipment from service</li></ul>
            """,
        },
    }
    for slug, values in blog_translations.items():
        values["author_name_en"] = "Vazneh Research and Development Team"
        BlogPost.objects.filter(slug=slug).update(**values)


def clear_english_content(apps, schema_editor):
    model_names_and_fields = {
        "ProductType": ("title_en",),
        "Product": (
            "title_en",
            "subtitle_en",
            "short_description_en",
            "detailed_description_en",
        ),
        "ProductCapacity": ("title_en",),
        "ProductSize": ("title_en",),
        "ProductFeature": ("title_en",),
        "Project": ("title_en", "subtitle_en", "description_en", "location_en"),
        "ProjectFeature": ("title_en",),
        "Representative": ("name_en", "city_en", "address_en"),
        "Service": (
            "title_en",
            "subtitle_en",
            "short_description_en",
            "detailed_description_en",
        ),
        "ServiceItem": ("title_en", "description_en"),
        "BlogPost": ("title_en", "excerpt_en", "body_en", "author_name_en"),
    }
    for model_name, fields in model_names_and_fields.items():
        model = apps.get_model("main", model_name)
        model.objects.update(**{field: "" for field in fields})


class Migration(migrations.Migration):
    dependencies = [("main", "0014_add_english_content")]

    operations = [
        migrations.RunPython(populate_english_content, clear_english_content),
    ]
