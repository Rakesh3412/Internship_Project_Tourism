import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tourism_app.models import State, Category, TouristPlace, PlaceImage, Review, TripInquiry


class Command(BaseCommand):
    help = 'Seeds database with realistic, high-quality tourism states, places, categories, reviews, and admin user'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("[*] Starting Tourism Database Seeding..."))

        # 1. Create Superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@tourvista.com', 'admin123')
            self.stdout.write(self.style.SUCCESS("[OK] Admin user created (Username: admin, Password: admin123)"))
        else:
            self.stdout.write("[OK] Admin user already exists.")

        # 2. Seed Categories
        categories_data = [
            {
                'name': 'Heritage & Forts',
                'icon': 'fa-monument',
                'image_url': 'https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800&auto=format&fit=crop',
                'description': 'Ancient palaces, majestic UNESCO forts, rock-cut architecture, and royal heritage.'
            },
            {
                'name': 'Hill Stations & Mountains',
                'icon': 'fa-mountain',
                'image_url': 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=800&auto=format&fit=crop',
                'description': 'Mist-covered peaks, lush tea gardens, pine valleys, snow viewpoints, and tranquil getaways.'
            },
            {
                'name': 'Beaches & Coastal',
                'icon': 'fa-umbrella-beach',
                'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&auto=format&fit=crop',
                'description': 'Golden sand stretches, turquoise waters, vibrant beach shacks, watersports, and stunning sunsets.'
            },
            {
                'name': 'Nature & Backwaters',
                'icon': 'fa-water',
                'image_url': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=800&auto=format&fit=crop',
                'description': 'Serene palm-fringed canals, luxury houseboats, emerald lagoons, and tranquil waterways.'
            },
            {
                'name': 'Spiritual & Pilgrimage',
                'icon': 'fa-om',
                'image_url': 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=800&auto=format&fit=crop',
                'description': 'Sacred ghats, historic temple complexes, spiritual ashrams, and timeless rituals.'
            },
            {
                'name': 'Wildlife & National Parks',
                'icon': 'fa-paw',
                'image_url': 'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=800&auto=format&fit=crop',
                'description': 'Thriving tiger reserves, elephant corridors, exotic bird sanctuaries, and thrilling jungle safaris.'
            },
            {
                'name': 'Adventure & Trekking',
                'icon': 'fa-hiking',
                'image_url': 'https://images.unsplash.com/photo-1527631746610-bca00a040d60?w=800&auto=format&fit=crop',
                'description': 'White water rafting, high-altitude trekking, paragliding, desert dune bashing, and ziplining.'
            },
        ]

        cats_dict = {}
        for cdata in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cdata['name'],
                defaults={
                    'icon': cdata['icon'],
                    'image_url': cdata['image_url'],
                    'description': cdata['description']
                }
            )
            cats_dict[cdata['name']] = cat
        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(cats_dict)} Categories."))

        # 3. Seed States
        states_data = [
            {
                'name': 'Kerala',
                'capital': 'Thiruvananthapuram',
                'tagline': "God's Own Country",
                'description': 'Kerala, a state on India\'s tropical Malabar Coast, has nearly 600km of Arabian Sea shoreline. It\'s renowned for its palm-lined beaches, backwaters network of canals, spice plantations, and Ayurvedic wellness retreats.',
                'history_culture': 'Rich with ancient maritime trade heritage, Kathakali classical dance, Kalaripayattu martial arts, and Onam festivities.',
                'best_time_to_visit': 'September to March',
                'climate': 'Tropical Monsoon & Coastal',
                'languages': 'Malayalam, English, Tamil',
                'cover_image_url': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=800&auto=format&fit=crop',
                'banner_image_url': 'https://images.unsplash.com/photo-1593693397690-362cb9666fc2?w=1600&auto=format&fit=crop',
                'is_featured': True
            },
            {
                'name': 'Rajasthan',
                'capital': 'Jaipur',
                'tagline': 'The Land of Kings & Grandeur',
                'description': 'Rajasthan is known for its royal palaces, imposing hill forts, vibrant desert festivals, and rich craftsmanship. From the pink city of Jaipur to the golden dunes of Jaisalmer, every corner radiates regal charisma.',
                'history_culture': 'Home to legendary Rajput valor, vibrant Ghoomar dance, intricate mirror-work handicrafts, and majestic royal palaces.',
                'best_time_to_visit': 'October to March',
                'climate': 'Semi-arid & Desert',
                'languages': 'Hindi, Rajasthani, Marwari, English',
                'cover_image_url': 'https://images.unsplash.com/photo-1477587458883-47145ed94245?w=800&auto=format&fit=crop',
                'banner_image_url': 'https://images.unsplash.com/photo-1599661046289-e31897846e41?w=1600&auto=format&fit=crop',
                'is_featured': True
            },
            {
                'name': 'Himachal Pradesh',
                'capital': 'Shimla',
                'tagline': 'Land of Gods & Snowy Peaks',
                'description': 'Himachal Pradesh is a northern Indian state in the Himalayas, celebrated for its scenic mountain towns, snow-capped ranges, river valleys, and adventure sports like paragliding, skiing, and trekking.',
                'history_culture': 'Deeply spiritual culture with ancient wooden pagoda temples, Tibetan Buddhist monasteries, and vibrant apple orchard communities.',
                'best_time_to_visit': 'All Year Round (Dec-Feb for Snow, Mar-Jun for Pleasant Summers)',
                'climate': 'Alpine & Cool Temperate',
                'languages': 'Hindi, Pahari, Kangri, English',
                'cover_image_url': 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=800&auto=format&fit=crop',
                'banner_image_url': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1600&auto=format&fit=crop',
                'is_featured': True
            },
            {
                'name': 'Goa',
                'capital': 'Panaji',
                'tagline': 'Pearl of the Orient & Beach Haven',
                'description': 'Goa is India\'s pocket-sized paradise on the western coast. Renowned for its sun-kissed beaches, Portuguese colonial architecture, pulsating nightlife, fresh seafood, and laid-back "susegad" lifestyle.',
                'history_culture': '450 years of Portuguese rule infused a unique Indo-Portuguese blend in architecture, culinary spices, carnivals, and Baroque churches.',
                'best_time_to_visit': 'November to February',
                'climate': 'Tropical Maritime',
                'languages': 'Konkani, Marathi, English, Portuguese',
                'cover_image_url': 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&auto=format&fit=crop',
                'banner_image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&auto=format&fit=crop',
                'is_featured': True
            },
            {
                'name': 'Karnataka',
                'capital': 'Bengaluru',
                'tagline': 'One State, Many Worlds',
                'description': 'Karnataka seamlessly marries silicon valleys with ancient rock-cut empires of Hampi, misty coffee estates of Coorg, pristine Arabian sea coastline, and rich royal heritage of Mysore.',
                'history_culture': 'Cradle of Vijayanagara, Hoysala, and Chalukya empires, famed for Carnatic music, Mysore silk, and world-class coffee.',
                'best_time_to_visit': 'October to April',
                'climate': 'Tropical & Subtropical',
                'languages': 'Kannada, English, Tulu',
                'cover_image_url': 'https://images.unsplash.com/photo-1600100397608-f010f443b749?w=800&auto=format&fit=crop',
                'banner_image_url': 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=1600&auto=format&fit=crop',
                'is_featured': True
            },
            {
                'name': 'Uttarakhand',
                'capital': 'Dehradun',
                'tagline': 'Devbhoomi - The Abode of Gods',
                'description': 'Nestled in the lap of the mighty Himalayas, Uttarakhand is world-renowned for the holy Ganges ghats in Rishikesh, high Himalayan trekking trails, Jim Corbett tiger sanctuary, and alpine flower meadows.',
                'history_culture': 'Sacred epicenter of Vedic spirituality, yoga, Ayurveda, and the sacred Char Dham pilgrimage trails.',
                'best_time_to_visit': 'March to June & September to November',
                'climate': 'Alpine & Temperate',
                'languages': 'Hindi, Garhwali, Kumaoni, English',
                'cover_image_url': 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=800&auto=format&fit=crop',
                'banner_image_url': 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=1600&auto=format&fit=crop',
                'is_featured': True
            },
            {
                'name': 'Tamil Nadu',
                'capital': 'Chennai',
                'tagline': 'Timeless Heritage & Living Traditions',
                'description': 'Tamil Nadu boasts over 33,000 ancient temples with sky-high sculpted Gopurams, serene hill stations like Ooty and Kodaikanal, and the southernmost tip of peninsular India where three oceans meet.',
                'history_culture': 'Home of the ancient Dravidian civilization, Chola bronze masterpieces, Bharatanatyam dance, and Carnatic music.',
                'best_time_to_visit': 'November to March',
                'climate': 'Tropical Wet & Dry',
                'languages': 'Tamil, English',
                'cover_image_url': 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=800&auto=format&fit=crop',
                'banner_image_url': 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=1600&auto=format&fit=crop',
                'is_featured': False
            },
        ]

        states_dict = {}
        for sdata in states_data:
            st, created = State.objects.get_or_create(
                name=sdata['name'],
                defaults=sdata
            )
            states_dict[sdata['name']] = st
        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(states_dict)} States."))

        # 4. Seed Tourist Places
        places_data = [
            # KERALA
            {
                'state': 'Kerala',
                'category': 'Hill Stations & Mountains',
                'name': 'Munnar Tea Plantations & Anamudi',
                'city': 'Munnar',
                'short_summary': 'Rolling emerald tea hills, misty valleys, crisp mountain air, and exotic flora in the Western Ghats.',
                'detailed_description': 'Situated at an altitude of 1,600 meters, Munnar is Kerala\'s most celebrated hill station. Once the summer resort of the British administration, it is enveloped by sprawling tea estates, colonial bungalows, cascading waterfalls, and Anamudi, the highest peak in South India. Travelers love trekking the lockhart gap, exploring tea factories, and spotting Nilgiri Tahr.',
                'highlights': 'Tea Museum & Factory Tours, Mattupetty Dam Boating, Top Station Viewpoint, Eravikulam National Park Nilgiri Tahr spotting, Spice Plantation Walk.',
                'address': 'Munnar Hill Station, Idukki District, Kerala - 685612',
                'latitude': 10.0889,
                'longitude': 77.0595,
                'entry_fee': 'Free (Eravikulam Park: ₹200)',
                'timings': 'Open 24 Hours (Attractions: 08:30 AM - 05:00 PM)',
                'best_season': 'September to May',
                'how_to_reach_air': 'Cochin International Airport (COK) - 110 km (approx 3.5 hrs drive)',
                'how_to_reach_train': 'Aluva Railway Station - 110 km / Ernakulam Junction - 130 km',
                'how_to_reach_road': 'Scenic NH-85 connected directly from Kochi, Madurai, and Coimbatore.',
                'rating': 4.9,
                'cover_image_url': 'https://images.unsplash.com/photo-1593693397690-362cb9666fc2?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': True,
                'gallery': [
                    ('https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=800&auto=format&fit=crop', 'Sunrise over misty Munnar tea slopes'),
                    ('https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=800&auto=format&fit=crop', 'Scenic viewpoint overlooking Western Ghats')
                ]
            },
            {
                'state': 'Kerala',
                'category': 'Nature & Backwaters',
                'name': 'Alleppey Backwaters & Kettuvallam',
                'city': 'Alappuzha',
                'short_summary': 'Glide through palm-fringed canals, paddy fields, and tranquil lagoons aboard traditional thatched houseboats.',
                'detailed_description': 'Known affectionately as the "Venice of the East", Alleppey is the heart of Kerala\'s famous backwaters. A cruise in a traditional motorized Kettuvallam houseboat offering freshly prepared Karimeen Pollichathu (pearl spot fish) and tender coconut is a quintessential Kerala experience.',
                'highlights': 'Luxury Houseboat Overnight Stay, Shikara Canal Rides, Punnamada Lake Snake Boat Races, Marari Beach Sunset.',
                'address': 'Finishing Point, Punnamada, Alappuzha, Kerala - 688013',
                'latitude': 9.4981,
                'longitude': 76.3388,
                'entry_fee': 'Shikara: ₹600/hr, Houseboat: ₹8,000 - ₹20,000/night',
                'timings': 'Day Cruises: 09:00 AM - 05:30 PM',
                'best_season': 'October to March',
                'how_to_reach_air': 'Cochin International Airport (COK) - 85 km',
                'how_to_reach_train': 'Alappuzha Railway Station (ALLP) - 3 km from jetty',
                'how_to_reach_road': 'Connected via NH-66 from Kochi (55 km) and Trivandrum (150 km).',
                'rating': 4.8,
                'cover_image_url': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': True,
                'gallery': [
                    ('https://images.unsplash.com/photo-1593693397690-362cb9666fc2?w=800&auto=format&fit=crop', 'Houseboat cruising calm emerald waters')
                ]
            },
            {
                'state': 'Kerala',
                'category': 'Beaches & Coastal',
                'name': 'Kovalam Lighthouse Beach',
                'city': 'Thiruvananthapuram',
                'short_summary': 'Crescent-shaped sandy beaches flanked by swaying coconut palms and a majestic red-and-white striped lighthouse.',
                'detailed_description': 'Kovalam is an internationally famous coastal town featuring three adjacent crescent beaches. The southernmost Lighthouse Beach offers panoramic Arabian sea views from the 30-meter Vizhinjam Lighthouse, beachfront seafood bistros, surfing lessons, and Ayurvedic massage centers.',
                'highlights': 'Climb the 118-foot Lighthouse, Surfing at Hawah Beach, Sunset Dining on the Promenade, Ayurvedic Rejuvenation.',
                'address': 'Lighthouse Beach Road, Kovalam, Thiruvananthapuram, Kerala - 695527',
                'latitude': 8.3988,
                'longitude': 76.9785,
                'entry_fee': 'Free (Lighthouse: ₹20)',
                'timings': 'Open 24 Hours (Lighthouse: 10:00 AM - 05:00 PM)',
                'best_season': 'November to February',
                'how_to_reach_air': 'Trivandrum International Airport (TRV) - 15 km',
                'how_to_reach_train': 'Trivandrum Central (TVC) - 16 km',
                'how_to_reach_road': 'Frequent taxis, buses, and autos from Thiruvananthapuram city.',
                'rating': 4.7,
                'cover_image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&auto=format&fit=crop',
                'is_popular': False,
                'is_featured': False,
                'gallery': []
            },

            # RAJASTHAN
            {
                'state': 'Rajasthan',
                'category': 'Heritage & Forts',
                'name': 'Amer Fort & Sheesh Mahal',
                'city': 'Jaipur',
                'short_summary': 'An imposing 16th-century hilltop fortress with intricate mirror palaces, Mughal gardens, and elephant courtyards.',
                'detailed_description': 'Amer Fort, perched high on the rugged Cheel ka Teela (Hill of Eagles), is a UNESCO World Heritage Site overlooking the Maota Lake. Built by Raja Man Singh I in red sandstone and marble, it contains stunning courtyards like Diwan-e-Aam, and the dazzling Sheesh Mahal (Hall of Mirrors) where a single candle illuminates the entire chamber.',
                'highlights': 'Sheesh Mahal mirror mosaics, Diwan-e-Khas, Evening Sound & Light Show, Elephant Ride, Panoramic view of Maota Lake.',
                'address': 'Devisinghpura, Amer, Jaipur, Rajasthan - 302001',
                'latitude': 26.9855,
                'longitude': 75.8513,
                'entry_fee': 'Indians: ₹100, Foreigners: ₹550, Students: ₹20',
                'timings': '08:00 AM - 05:30 PM & Night Tour 06:30 PM - 09:15 PM',
                'best_season': 'October to March',
                'how_to_reach_air': 'Jaipur International Airport (JAI) - 22 km',
                'how_to_reach_train': 'Jaipur Junction (JP) - 13 km',
                'how_to_reach_road': 'Located along Delhi-Jaipur highway NH-48; well connected by city buses and cabs.',
                'rating': 4.9,
                'cover_image_url': 'https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': True,
                'gallery': [
                    ('https://images.unsplash.com/photo-1477587458883-47145ed94245?w=800&auto=format&fit=crop', 'Amer Fort reflecting in Maota Lake'),
                    ('https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=800&auto=format&fit=crop', 'Intricate carvings and royal pavilions')
                ]
            },
            {
                'state': 'Rajasthan',
                'category': 'Heritage & Forts',
                'name': 'City Palace & Lake Pichola',
                'city': 'Udaipur',
                'short_summary': 'Romantic lakeside palaces, floating marble wonders, and breathtaking royal balconies overlooking the Aravalli hills.',
                'detailed_description': 'Known as the "Venice of the East", Udaipur\'s City Palace complex is a colossal marvel constructed over 400 years on the eastern banks of Lake Pichola. A boat cruise during twilight offers magical views of the Jag Mandir and the world-famous Lake Palace illuminated against dark waters.',
                'highlights': 'Sunset Boat Ride on Lake Pichola, Mor Chowk peacock mosaics, Crystal Gallery, Vintage Car Collection.',
                'address': 'Old City, Udaipur, Rajasthan - 313001',
                'latitude': 24.5764,
                'longitude': 73.6835,
                'entry_fee': 'Adults: ₹300, Children: ₹100, Boat Ride: ₹450',
                'timings': '09:30 AM - 05:30 PM',
                'best_season': 'September to March',
                'how_to_reach_air': 'Maharana Pratap Airport (UDR) - 24 km',
                'how_to_reach_train': 'Udaipur City Railway Station (UDZ) - 3 km',
                'how_to_reach_road': 'Excellent 4-lane highways connecting Ahmedabad, Jaipur, and Delhi.',
                'rating': 4.9,
                'cover_image_url': 'https://images.unsplash.com/photo-1477587458883-47145ed94245?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': True,
                'gallery': [
                    ('https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800&auto=format&fit=crop', 'Lake Pichola sunset with palace reflection')
                ]
            },
            {
                'state': 'Rajasthan',
                'category': 'Adventure & Trekking',
                'name': 'Sam Sand Dunes Desert Safari',
                'city': 'Jaisalmer',
                'short_summary': 'Golden desert dunes, camel safaris, traditional Kalbelia folk performances, and stargazing under crisp desert skies.',
                'detailed_description': 'Located 40 km from the Golden City of Jaisalmer, Sam Sand Dunes offer 30-to-60-meter high undulating dunes in the Thar Desert. Experience thrill-packed 4x4 dune bashing, traditional camel caravans at sunset, Rajasthani buffet dinners in luxury Swiss tents, and nocturnal astronomy.',
                'highlights': 'Jeep Dune Bashing, Sunset Camel Safari, Cultural Campfires with Folk Dancers, Desert Glamping.',
                'address': 'Sam Sand Dunes, Jaisalmer, Rajasthan - 345001',
                'latitude': 26.8286,
                'longitude': 70.5218,
                'entry_fee': 'Camel Ride: ₹500, Jeep Safari: ₹1,500, Camp: ₹3,000+',
                'timings': 'Safaris: 05:00 AM - 08:00 AM & 04:00 PM - 07:30 PM',
                'best_season': 'November to February',
                'how_to_reach_air': 'Jaisalmer Airport (JSA) - 50 km',
                'how_to_reach_train': 'Jaisalmer Railway Station (JSM) - 42 km',
                'how_to_reach_road': 'Direct paved desert highway from Jaisalmer fort city.',
                'rating': 4.8,
                'cover_image_url': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&auto=format&fit=crop',
                'is_popular': False,
                'is_featured': False,
                'gallery': []
            },

            # HIMACHAL PRADESH
            {
                'state': 'Himachal Pradesh',
                'category': 'Adventure & Trekking',
                'name': 'Solang Valley & Rohtang Pass',
                'city': 'Manali',
                'short_summary': 'Glacier peaks, year-round snow activities, paragliding, skiing, and thrilling mountain passes.',
                'detailed_description': 'Solang Valley, 14 km from Manali, is the adventure hub of Himachal Pradesh. Surrounded by snow-covered Himalayan peaks, it offers paragliding, zorbing, ATV quad biking, and skiing in winter. Further up, the legendary Rohtang Pass at 3,978 meters provides breathtaking panoramas of the Pir Panjal range and Lahaul Valley.',
                'highlights': 'Tandem Paragliding over snowy slopes, Atal Tunnel Drive, Snow Scooter Rides, Solang Ropeway Cable Car.',
                'address': 'Solang Valley, Manali, Kullu District, Himachal Pradesh - 175131',
                'latitude': 32.3166,
                'longitude': 77.1593,
                'entry_fee': 'Solang Entry: Free (Activities from ₹500 - ₹3,500; Rohtang Permit: ₹550)',
                'timings': '09:00 AM - 06:00 PM',
                'best_season': 'December to March (Snow), April to June (Summer Sports)',
                'how_to_reach_air': 'Kullu-Manali Airport at Bhuntar (KUU) - 50 km',
                'how_to_reach_train': 'Chandigarh Railway Station (CDG) - 310 km',
                'how_to_reach_road': 'Well serviced by luxury Volvo buses from Delhi (530 km) and Chandigarh.',
                'rating': 4.9,
                'cover_image_url': 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': True,
                'gallery': [
                    ('https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&auto=format&fit=crop', 'Panoramic snow-clad Himalayan mountain peaks')
                ]
            },
            {
                'state': 'Himachal Pradesh',
                'category': 'Hill Stations & Mountains',
                'name': 'The Ridge & Mall Road Shimla',
                'city': 'Shimla',
                'short_summary': 'Colonial British architecture, Christ Church neo-gothic spire, wooden toy train, and sweeping mountain vistas.',
                'detailed_description': 'The Ridge is the wide open cultural hub in the heart of Shimla, connecting the famous Mall Road, Lakkar Bazaar, and Scandal Point. Built during the British colonial era when Shimla was the summer capital of British India, it offers panoramic vistas of the snow-capped Himalayan ranges.',
                'highlights': 'Heritage UNESCO Kalka-Shimla Toy Train ride, Christ Church stained glass windows, Jakhoo Hanuman Temple ropeway, Lakkar Bazaar wooden craft.',
                'address': 'The Ridge, Mall Road, Shimla, Himachal Pradesh - 171001',
                'latitude': 31.1048,
                'longitude': 77.1734,
                'entry_fee': 'Free',
                'timings': 'Open 24 Hours (Shops: 10:00 AM - 09:00 PM)',
                'best_season': 'March to June & December to February (Snowfall)',
                'how_to_reach_air': 'Jubarhatti Airport Shimla (SLV) - 22 km / Chandigarh (IXC) - 120 km',
                'how_to_reach_train': 'Shimla Railway Station (SML) via Kalka Toy Train',
                'how_to_reach_road': 'Smooth 4-lane Himalayan expressway from Chandigarh (110 km).',
                'rating': 4.7,
                'cover_image_url': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': False,
                'gallery': []
            },

            # GOA
            {
                'state': 'Goa',
                'category': 'Beaches & Coastal',
                'name': 'Baga & Calangute Beach',
                'city': 'North Goa',
                'short_summary': 'Lively golden sands, parasailing, jet skis, beach shacks, seafood grills, and vibrant nightlife.',
                'detailed_description': 'Calangute and Baga form the beating heart of North Goa\'s coastal tourism. Known as the "Queen of Beaches", Calangute offers sprawling sands lined with sunbeds, water sports operators, and beach clubs like Tito\'s and Britto\'s serving fresh butter garlic prawns and cold drinks.',
                'highlights': 'Parasailing & Jet Skiing, Dolphin spotting boat trips, Sunset beach parties at Baga Creek, Saturday Night Market.',
                'address': 'Calangute - Baga Beach Road, North Goa, Goa - 403516',
                'latitude': 15.5439,
                'longitude': 73.7554,
                'entry_fee': 'Free (Water sports package: ₹1,500 - ₹2,500)',
                'timings': 'Open 24 Hours',
                'best_season': 'October to April',
                'how_to_reach_air': 'Manohar International Airport, Mopa (GOX) - 30 km / Dabolim (GOI) - 40 km',
                'how_to_reach_train': 'Thivim Railway Station (THVM) - 18 km / Madgaon (MAO) - 50 km',
                'how_to_reach_road': 'Accessible by rented self-drive scooters, taxis, and state buses.',
                'rating': 4.8,
                'cover_image_url': 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': True,
                'gallery': [
                    ('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&auto=format&fit=crop', 'Sunset over Baga beach coastline')
                ]
            },
            {
                'state': 'Goa',
                'category': 'Nature & Backwaters',
                'name': 'Dudhsagar 4-Tier Waterfalls',
                'city': 'Sonaulim',
                'short_summary': 'One of India\'s tallest four-tiered waterfalls cascading like a sea of white milk through lush Western Ghat jungles.',
                'detailed_description': 'Dudhsagar (meaning "Sea of Milk") is a spectacular 310-meter waterfall located on the Mandovi River along the Goa-Karnataka border. Surrounded by the dense Bhagwan Mahaveer Wildlife Sanctuary, the adventurous journey involves open-top 4x4 forest jeep safari crossing mountain streams and natural freshwater pools.',
                'highlights': '4x4 Jungle Jeep Safari, Swimming in natural freshwater pool with lifejackets, Bhagwan Mahaveer Wildlife Sanctuary safari, iconic railway bridge photography.',
                'address': 'Sonaulim, Goa - 403410',
                'latitude': 15.3144,
                'longitude': 74.3143,
                'entry_fee': 'Forest Entry: ₹100 + Jeep Safari: ₹3,500 (per vehicle for 7 people)',
                'timings': '08:30 AM - 04:30 PM (Closed during peak monsoon floods)',
                'best_season': 'October to March (Post-monsoon full flow)',
                'how_to_reach_air': 'Dabolim Airport (GOI) - 70 km',
                'how_to_reach_train': 'Kulem Railway Station (QLM) - 12 km (jeep boarding point)',
                'how_to_reach_road': 'Drive to Kulem/Mollem taxi stand via NH-748 from Panaji or Margao.',
                'rating': 4.9,
                'cover_image_url': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': False,
                'gallery': []
            },
            {
                'state': 'Goa',
                'category': 'Heritage & Forts',
                'name': 'Fort Aguada & 17th Century Lighthouse',
                'city': 'Candolim',
                'short_summary': 'Portuguese sea fortress built in 1612 with panoramic views of the Arabian Sea and Sinquerim beach.',
                'detailed_description': 'Fort Aguada is a well-preserved 17th-century Portuguese fortress standing on the beach south of Candolim at the shore of the Mandovi River. Its grand freshwater spring once provided fresh water to passing ships, giving the fort its name "Aguada" (Water).',
                'highlights': 'Old 4-tiered Lighthouse, Jail Museum, Sunset views over Panaji bay, Portuguese battlements.',
                'address': 'Aguada Fort Area, Candolim, Goa - 403515',
                'latitude': 15.4920,
                'longitude': 73.7737,
                'entry_fee': 'Indians: ₹25, Foreigners: ₹300',
                'timings': '09:00 AM - 06:00 PM',
                'best_season': 'October to March',
                'how_to_reach_air': 'Mopa Airport (GOX) - 35 km / Dabolim (GOI) - 42 km',
                'how_to_reach_train': 'Thivim (THVM) - 22 km',
                'how_to_reach_road': 'Located 15 km from Panaji, reachable by taxi or rented bike.',
                'rating': 4.6,
                'cover_image_url': 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&auto=format&fit=crop',
                'is_popular': False,
                'is_featured': False,
                'gallery': []
            },

            # KARNATAKA
            {
                'state': 'Karnataka',
                'category': 'Heritage & Forts',
                'name': 'Hampi UNESCO Ruins & Stone Chariot',
                'city': 'Hampi / Hospet',
                'short_summary': 'A breathtaking boulder-strewn open-air museum of the grand 14th-century Vijayanagara Empire.',
                'detailed_description': 'Hampi is a UNESCO World Heritage Site nestled along the banks of the Tungabhadra River. The ruins of the Vijayanagara Empire boast majestic monolithic structures, musical pillars at the Vijaya Vittala Temple, the iconic stone chariot, and breathtaking sunsets from Matanga Hill.',
                'highlights': 'Vijaya Vittala Stone Chariot & Musical Pillars, Virupaksha Temple, Coracle boat rides on Tungabhadra, Matanga Hill sunrise trek.',
                'address': 'Hampi, Vijayanagara District, Karnataka - 583239',
                'latitude': 15.3350,
                'longitude': 76.4600,
                'entry_fee': 'Indians: ₹40, Foreigners: ₹600',
                'timings': '06:00 AM - 06:00 PM',
                'best_season': 'October to March',
                'how_to_reach_air': 'Hubli Airport (HBX) - 140 km / Jindal Vidyanagar Airport (VDY) - 40 km',
                'how_to_reach_train': 'Hosapete Junction (HPT) - 13 km',
                'how_to_reach_road': 'Connected by NH-50 and NH-67 from Bengaluru (340 km) and Goa (310 km).',
                'rating': 4.9,
                'cover_image_url': 'https://images.unsplash.com/photo-1600100397608-f010f443b749?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': True,
                'gallery': [
                    ('https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800&auto=format&fit=crop', 'Iconic stone chariot of Vittala temple at sunrise')
                ]
            },
            {
                'state': 'Karnataka',
                'category': 'Hill Stations & Mountains',
                'name': 'Coorg / Kodagu Coffee Hills & Abbey Falls',
                'city': 'Madikeri (Coorg)',
                'short_summary': 'Scotland of India: lush coffee plantations, spice trails, gushing waterfalls, and Kodava hospitality.',
                'detailed_description': 'Coorg is a tranquil hill haven perched on the slopes of the Western Ghats. Famed for its aromatic Arabica and Robusta coffee estates, cardamom groves, Tibetan settlement at Bylakuppe, and misty mountain viewpoints like Raja\'s Seat.',
                'highlights': 'Abbey Falls & Iruppu Falls, Namdroling Monastery Golden Temple, Raja\'s Seat Sunset, Coffee Estate Homestay Experience.',
                'address': 'Madikeri, Kodagu District, Karnataka - 571201',
                'latitude': 12.4244,
                'longitude': 75.7382,
                'entry_fee': 'Abbey Falls: ₹20, Monasteries: Free',
                'timings': '08:00 AM - 06:00 PM',
                'best_season': 'September to May',
                'how_to_reach_air': 'Kannur International Airport (CNN) - 90 km / Mangalore (IXE) - 140 km',
                'how_to_reach_train': 'Mysuru Railway Station (MYS) - 115 km',
                'how_to_reach_road': 'Direct scenic road from Bengaluru (250 km) and Mysuru.',
                'rating': 4.8,
                'cover_image_url': 'https://images.unsplash.com/photo-1593693397690-362cb9666fc2?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': False,
                'gallery': []
            },
            {
                'state': 'Karnataka',
                'category': 'Heritage & Forts',
                'name': 'Mysore Palace & Illuminations',
                'city': 'Mysuru',
                'short_summary': 'Indo-Saracenic royal palace glowing with 100,000 incandescent bulbs on Sunday evenings.',
                'detailed_description': 'Mysore Palace is the official residence of the Wadiyar dynasty. Designed by British architect Henry Irwin, this three-story stone palace with marble domes features an ornate Durbar Hall, carved mahogany ceilings, and stained-glass peacock skylights.',
                'highlights': 'Grand Sunday Evening Illumination with 100k lights, Kalyana Mantapa stained glass dome, Golden Throne, Dussehra procession grounds.',
                'address': 'Sayyaji Rao Rd, Agrahara, Chamrajpura, Mysuru, Karnataka - 570001',
                'latitude': 12.3052,
                'longitude': 76.6552,
                'entry_fee': 'Indians: ₹100, Foreigners: ₹300, Students: ₹50',
                'timings': '10:00 AM - 05:30 PM (Illumination: Sundays 07:00 PM - 07:45 PM)',
                'best_season': 'September to March (October for Mysore Dussehra)',
                'how_to_reach_air': 'Mysore Airport (MYQ) - 10 km / Bengaluru (BLR) - 170 km',
                'how_to_reach_train': 'Mysuru Junction (MYS) - 2 km',
                'how_to_reach_road': 'Smooth Bengaluru-Mysuru 10-lane expressway (2 hrs drive).',
                'rating': 4.9,
                'cover_image_url': 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': False,
                'gallery': []
            },

            # UTTARAKHAND
            {
                'state': 'Uttarakhand',
                'category': 'Spiritual & Pilgrimage',
                'name': 'Rishikesh Ganga Aarti & River Rafting',
                'city': 'Rishikesh',
                'short_summary': 'The Yoga Capital of the World, sacred Triveni Ghat aarti, Laxman Jhula, and thrilling grade-4 white water rafting.',
                'detailed_description': 'Situated along the holy Ganges where it descends from the Himalayas into the plains, Rishikesh is a global hub for yoga, meditation, spirituality, and adrenaline-pumping adventures. Witness the mesmerizing sunset Ganga Aarti at Triveni Ghat and experience river rafting from Shivpuri down to Marine Drive.',
                'highlights': 'Triveni Ghat Evening Aarti, White Water Rafting (16km/24km), Ram Jhula & Beatles Ashram (Chaurasi Kutia), Cliff Jumping.',
                'address': 'Triveni Ghat / Tapovan, Rishikesh, Uttarakhand - 249201',
                'latitude': 30.0869,
                'longitude': 78.2676,
                'entry_fee': 'Ghats: Free, Rafting: ₹600 - ₹1,500/person, Beatles Ashram: ₹150',
                'timings': 'Open 24 Hours (Aarti: 06:00 PM - 07:15 PM)',
                'best_season': 'September to May (Rafting closed during July-Aug monsoon)',
                'how_to_reach_air': 'Jolly Grant Airport, Dehradun (DED) - 20 km',
                'how_to_reach_train': 'Yog Nagari Rishikesh (YNRK) / Haridwar (HW) - 25 km',
                'how_to_reach_road': 'Delhi-Meerut Expressway and NH-334 (4.5 hrs from Delhi).',
                'rating': 4.9,
                'cover_image_url': 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': True,
                'gallery': [
                    ('https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&auto=format&fit=crop', 'Ganga Aarti with floating diyas at twilight')
                ]
            },
            {
                'state': 'Uttarakhand',
                'category': 'Wildlife & National Parks',
                'name': 'Jim Corbett National Park Jungle Safari',
                'city': 'Ramnagar',
                'short_summary': 'India\'s oldest national park, home to the elusive Royal Bengal Tiger, wild elephants, and rich flora.',
                'detailed_description': 'Established in 1936 as Hailey National Park, Jim Corbett is renowned as the birthplace of Project Tiger. Spanning 520 square kilometers of hills, marshy depressions, riverine belts, and grassland, zones like Dhikala, Bijrani, and Jhirna provide high chances of spotting Royal Bengal Tigers in the wild.',
                'highlights': 'Open Jeep Safari in Dhikala & Bijrani Zones, Stay inside Forest Rest House, Kosi River Angling, Birdwatching over 600 species.',
                'address': 'Ramnagar, Nainital District, Uttarakhand - 244715',
                'latitude': 29.5300,
                'longitude': 78.7747,
                'entry_fee': 'Safari Jeep (6 persons): ₹4,500 - ₹6,500 per trip',
                'timings': 'Morning Safari: 06:00 AM - 09:30 AM | Afternoon Safari: 02:30 PM - 06:00 PM',
                'best_season': 'November to June (Dhikala zone opens Nov 15)',
                'how_to_reach_air': 'Pantnagar Airport (PGH) - 80 km / Delhi (DEL) - 260 km',
                'how_to_reach_train': 'Ramnagar Railway Station (RMR) - 12 km',
                'how_to_reach_road': 'Connected via NH-309 from Delhi (approx 5.5 hours drive).',
                'rating': 4.8,
                'cover_image_url': 'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': False,
                'gallery': []
            },

            # TAMIL NADU
            {
                'state': 'Tamil Nadu',
                'category': 'Spiritual & Pilgrimage',
                'name': 'Meenakshi Amman Temple',
                'city': 'Madurai',
                'short_summary': 'Historic 2,500-year-old temple complex with 14 towering sculpted Gopurams and the Hall of Thousand Pillars.',
                'detailed_description': 'Meenakshi Sundareswarar Temple in Madurai is a masterwork of Dravidian architecture. Its 14 multicolored gopuram gateway towers rise up to 52 meters, adorned with thousands of colorful mythological figures, stone carvings, and the divine Golden Lotus Pond.',
                'highlights': 'Hall of 1000 Pillars, Golden Lotus Pond (Potramarai Kulam), Night Palliarai procession ceremony, intricate ceiling paintings.',
                'address': 'Madurai Main, Madurai, Tamil Nadu - 625001',
                'latitude': 9.9195,
                'longitude': 78.1193,
                'entry_fee': 'Free (Special Darshan: ₹100, Thousand Pillar Hall: ₹50)',
                'timings': '05:00 AM - 12:30 PM & 04:00 PM - 10:00 PM',
                'best_season': 'October to March',
                'how_to_reach_air': 'Madurai International Airport (IXM) - 12 km',
                'how_to_reach_train': 'Madurai Junction (MDU) - 1.5 km',
                'how_to_reach_road': 'Major highways connect Madurai to Chennai, Bangalore, and Kochi.',
                'rating': 4.9,
                'cover_image_url': 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=800&auto=format&fit=crop',
                'is_popular': True,
                'is_featured': False,
                'gallery': []
            },
            {
                'state': 'Tamil Nadu',
                'category': 'Hill Stations & Mountains',
                'name': 'Ooty Nilgiri Mountain Toy Train & Botanical Gardens',
                'city': 'Udhagamandalam (Ooty)',
                'short_summary': 'Queen of Nilgiri hill stations, UNESCO steam toy train, sprawling 55-acre botanical gardens, and Doddabetta peak.',
                'detailed_description': 'Perched at 2,240 meters in the Nilgiri Hills, Ooty is famed for the UNESCO-inscribed Nilgiri Mountain Railway steam train chugging past 16 tunnels and 250 bridges. Walk through century-old government botanical gardens and enjoy boating on the calm waters of Ooty Lake.',
                'highlights': 'UNESCO Nilgiri Mountain Toy Train, Government Botanical Gardens, Doddabetta Peak (2,637m), Pykara Waterfalls & Boating.',
                'address': 'Vannarapettai, Ooty, Tamil Nadu - 643002',
                'latitude': 11.4102,
                'longitude': 76.6950,
                'entry_fee': 'Botanical Garden: ₹50, Toy Train: ₹30 - ₹205',
                'timings': '07:00 AM - 06:30 PM',
                'best_season': 'October to June',
                'how_to_reach_air': 'Coimbatore International Airport (CJB) - 88 km',
                'how_to_reach_train': 'Mettupalayam (MTP) / Udagamandalam (UAM)',
                'how_to_reach_road': 'Scenic hair-pin bend drive through Nilgiri Ghat road from Coimbatore.',
                'rating': 4.8,
                'cover_image_url': 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=800&auto=format&fit=crop',
                'is_popular': False,
                'is_featured': False,
                'gallery': []
            }
        ]

        seeded_places = []
        for pdata in places_data:
            state_obj = states_dict[pdata['state']]
            cat_obj = cats_dict[pdata['category']]
            gallery_list = pdata.pop('gallery', [])

            place, created = TouristPlace.objects.get_or_create(
                name=pdata['name'],
                state=state_obj,
                defaults={
                    'category': cat_obj,
                    'city': pdata['city'],
                    'short_summary': pdata['short_summary'],
                    'detailed_description': pdata['detailed_description'],
                    'highlights': pdata['highlights'],
                    'address': pdata['address'],
                    'latitude': pdata['latitude'],
                    'longitude': pdata['longitude'],
                    'entry_fee': pdata['entry_fee'],
                    'timings': pdata['timings'],
                    'best_season': pdata['best_season'],
                    'how_to_reach_air': pdata['how_to_reach_air'],
                    'how_to_reach_train': pdata['how_to_reach_train'],
                    'how_to_reach_road': pdata['how_to_reach_road'],
                    'rating': pdata['rating'],
                    'cover_image_url': pdata['cover_image_url'],
                    'is_popular': pdata['is_popular'],
                    'is_featured': pdata['is_featured'],
                }
            )
            seeded_places.append(place)

            # Seed extra gallery images
            for img_url, caption in gallery_list:
                PlaceImage.objects.get_or_create(
                    place=place,
                    image_url=img_url,
                    defaults={'caption': caption}
                )

        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(seeded_places)} Tourist Places with Galleries."))

        # 5. Seed Reviews
        reviews_data = [
            {
                'place_name': 'Munnar Tea Plantations & Anamudi',
                'user_name': 'Aarav Sharma',
                'user_email': 'aarav@example.com',
                'rating': 5,
                'title': 'Pure Magic in the Western Ghats!',
                'comment': 'The fresh aroma of tea leaves and the chilly morning mist at Top Station are unforgettable. Renting a bicycle and cycling through the tea estates was the highlight of our trip!'
            },
            {
                'place_name': 'Alleppey Backwaters & Kettuvallam',
                'user_name': 'Elena Rostova',
                'user_email': 'elena@travelworld.com',
                'rating': 5,
                'title': 'An absolute dream experience!',
                'comment': 'Overnight stay in a private deluxe houseboat was relaxing beyond words. The freshly cooked fish curry and sunset over the tranquil canals are memories for life.'
            },
            {
                'place_name': 'Amer Fort & Sheesh Mahal',
                'user_name': 'Rajesh Singhania',
                'user_email': 'rajesh@example.com',
                'rating': 5,
                'title': 'Astonishing architecture & grandeur',
                'comment': 'The Sheesh Mahal is an engineering and artistic marvel. Do take an official audio guide or local historian to appreciate the rich stories behind each courtyard.'
            },
            {
                'place_name': 'Solang Valley & Rohtang Pass',
                'user_name': 'Priya Nair',
                'user_email': 'priya.n@example.com',
                'rating': 5,
                'title': 'Snow, thrills and breathtaking views!',
                'comment': 'Paragliding across Solang Valley with snow-capped peaks in front is breathtaking. The Atal tunnel made reaching Lahaul so easy and scenic.'
            },
            {
                'place_name': 'Hampi UNESCO Ruins & Stone Chariot',
                'user_name': 'David Miller',
                'user_email': 'david@wanderlust.com',
                'rating': 5,
                'title': 'Like stepping onto another planet',
                'comment': 'The boulder landscapes and intricate stone architecture of the Vijayanagara Empire are unparalleled. Sunset from Matanga Hill was magical.'
            },
            {
                'place_name': 'Rishikesh Ganga Aarti & River Rafting',
                'user_name': 'Sneha Mukherjee',
                'user_email': 'sneha@example.com',
                'rating': 5,
                'title': 'Soulful evenings and adrenaline mornings!',
                'comment': 'Grade 4 rafting from Marine Drive got my adrenaline pumping, followed by the deeply peaceful and divine evening Ganga Aarti at Triveni Ghat.'
            }
        ]

        for rdata in reviews_data:
            p_obj = TouristPlace.objects.filter(name__icontains=rdata['place_name'].split()[0]).first()
            if p_obj:
                Review.objects.get_or_create(
                    place=p_obj,
                    user_name=rdata['user_name'],
                    user_email=rdata['user_email'],
                    defaults={
                        'rating': rdata['rating'],
                        'title': rdata['title'],
                        'comment': rdata['comment'],
                        'is_approved': True,
                    }
                )
        self.stdout.write(self.style.SUCCESS("[OK] Seeded Verified Visitor Reviews."))

        # 6. Seed Sample Trip Inquiry
        sample_state = State.objects.filter(name='Kerala').first()
        sample_place = TouristPlace.objects.filter(name__icontains='Munnar').first()
        TripInquiry.objects.get_or_create(
            name='Kavita Krishnan',
            email='kavita.k@example.com',
            phone='+91 98765 43210',
            defaults={
                'destination_state': sample_state,
                'destination_place': sample_place,
                'travelers_count': 4,
                'budget_range': 'Moderate (Rs. 10,000 - 25,000)',
                'message': 'Looking for a 4-day customized family tour itinerary in Kerala including Munnar tea garden stay and 1 night Alleppey houseboat.',
                'status': 'Contacted'
            }
        )
        self.stdout.write(self.style.SUCCESS("[OK] Seeded Sample Trip Inquiries."))

        self.stdout.write(self.style.SUCCESS("[SUCCESS] Tourism Database Seeding Complete! Enjoy TourVista!"))

