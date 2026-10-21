# Gallatin area pages at /service-areas/<slug>/. Each needs its own unique text:
# near-duplicate location pages get treated by Google as "doorway pages" and hurt rankings.
# Fields: slug, name, title, desc, lead, about[], jobs[service slugs], map (Google Maps search text), nearby[slugs]

LOCATIONS = [
{
 "slug": "fairvue-plantation", "name": "Fairvue Plantation",
 "title": "Demolition & Junk Removal in Fairvue Plantation, Gallatin TN",
 "desc": "Demolition, junk removal and remodel protection for Fairvue Plantation homes in Gallatin, TN. Decks, interiors, landscaping and clean-outs. Free quotes.",
 "lead": "Careful, clean demolition and hauling for Fairvue Plantation's lake and golf course homes, with protection for the finishes that stay.",
 "about": [
  "Fairvue Plantation sits on the west side of Gallatin along Old Hickory Lake, built around the golf course and country club. Homes here range from established family homes to large lakefront properties, and many owners are updating kitchens, bathrooms and outdoor living spaces to match today's styles.",
  "We do a lot of deck and patio tear-outs for new outdoor living areas, interior demolition ahead of high-end kitchen and bath remodels, and landscape removal for redesigned yards. Because many Fairvue homes have premium finishes, we pair demolition with floor, surface and dust protection so nothing outside the work zone gets damaged. We also respect HOA rules on work hours, parking and debris, and keep trailers and equipment tidy and out of the way."
 ],
 "jobs": ["deck-removal", "kitchen-demolition", "bathroom-demolition", "landscape-removal", "remodeling-floor-protection", "concrete-removal"],
 "map": "Fairvue Plantation, Gallatin, TN",
 "nearby": ["station-camp", "nexus-south", "downtown-gallatin"]
},
{
 "slug": "downtown-gallatin", "name": "Downtown Gallatin",
 "title": "Demolition & Junk Removal in Downtown Gallatin, TN",
 "desc": "Interior demolition, clean-outs and junk removal for homes and storefronts in Downtown Gallatin, TN. Older-home know-how and tight-access work.",
 "lead": "Older homes, historic storefronts and tight streets around the square. Interior demolition, clean-outs and hauling, done with care for what makes downtown special.",
 "about": [
  "Downtown Gallatin, centered on the historic public square, has some of the oldest homes and commercial buildings in Sumner County. These properties have character, and they also have plaster walls, multiple layers of flooring, old wiring, cramped attics and crawlspaces, and limited parking and access.",
  "We help downtown homeowners and business owners with interior demolition for renovations, storefront and office strip-outs for new tenants, attic and crawlspace clean-outs, and estate clean-outs of older homes. Many older buildings were built before 1980 and may contain asbestos or lead paint, so we recommend testing before demolition and plan our work around the results. If your property is in a historic overlay area, exterior changes may require city review, so check with the City of Gallatin before removing porches, siding or other exterior features."
 ],
 "jobs": ["interior-demolition", "drywall-removal", "large-room-demolition", "attic-clean-out", "crawlspace-clean-out", "junk-removal"],
 "map": "Gallatin Public Square, Gallatin, TN",
 "nearby": ["airport-road", "kennesaw-farms", "fairvue-plantation"]
},
{
 "slug": "airport-road", "name": "Airport Road",
 "title": "Demolition & Junk Removal on Airport Road, Gallatin TN",
 "desc": "Demolition, junk removal and concrete removal for homes and businesses along the Airport Road corridor in Gallatin, TN, near Sumner County Regional Airport.",
 "lead": "Homes, businesses and larger lots along the Airport Road corridor. Outbuilding demolition, concrete removal, commercial clean-outs and hauling.",
 "about": [
  "The Airport Road corridor near Sumner County Regional Airport mixes residential streets with commercial, industrial and larger rural lots. That means a wide variety of jobs, from a homeowner clearing out a garage to a business removing old shelving, offices or a concrete pad.",
  "Along Airport Road we often remove outbuildings, carports and metal sheds, break out old concrete slabs and pads, haul away commercial junk and equipment, and do light commercial interior demolition for businesses moving in or out. We bring the right size trailer for the job and schedule around your business hours so operations aren't interrupted."
 ],
 "jobs": ["concrete-removal", "garage-demolition", "shed-removal", "large-room-demolition", "junk-removal", "exterior-demolition"],
 "map": "Airport Rd, Gallatin, TN",
 "nearby": ["downtown-gallatin", "dobbins-pike", "nexus-north"]
},
{
 "slug": "dobbins-pike", "name": "Dobbins Pike",
 "title": "Demolition & Junk Removal on Dobbins Pike, Gallatin TN",
 "desc": "Shed, barn, fence and outbuilding removal plus junk hauling for properties along Dobbins Pike in Gallatin, TN. Large-lot and rural property experts.",
 "lead": "Larger lots and country properties along Dobbins Pike. Old barns, sheds, fencing, outbuildings and years of accumulated junk cleared out.",
 "about": [
  "Properties along Dobbins Pike range from established homes to larger lots with more room to spread out, and room to spread out often means old sheds, small barns, carports, long runs of fencing and piles of materials that have built up over the years.",
  "We help Dobbins Pike property owners take down aging outbuildings, pull old wood and wire fencing (posts included), remove concrete pads and old foundations, clear brush and overgrown landscaping, and haul off scrap metal, old equipment and junk. Larger rural lots sometimes need longer carries or equipment access, and we plan for that up front so your quote is accurate."
 ],
 "jobs": ["shed-removal", "fence-removal", "garage-demolition", "landscape-removal", "concrete-removal", "junk-removal"],
 "map": "Dobbins Pike, Gallatin, TN",
 "nearby": ["airport-road", "nexus-north", "station-camp"]
},
{
 "slug": "nexus-north", "name": "Nexus North",
 "title": "Junk Removal & Demolition in Nexus North, Gallatin TN",
 "desc": "Junk removal, garage clean-outs, landscape removal and remodel protection for Nexus North homeowners in Gallatin, TN. Fast scheduling, free quotes.",
 "lead": "Newer homes, new projects. Move-in junk removal, garage clean-outs, landscape changes and protection for upgrades in Nexus North.",
 "about": [
  "Nexus North is one of Gallatin's newer residential areas, and newer homes come with their own kind of projects. Homeowners are finishing basements and bonus rooms, upgrading builder-grade kitchens and baths, adding patios and fences, and replacing starter landscaping with something more personal.",
  "In Nexus North we often haul away move-in boxes and leftover builder materials, clear out garages, remove builder-grade landscaping and rock, and remove fixtures or flooring ahead of upgrades. Because these homes have new finishes, we take protection seriously, covering floors, countertops and door frames so upgrades don't damage what's already new. We keep trailers neat and follow any HOA rules on parking and work hours."
 ],
 "jobs": ["junk-removal", "garage-clean-out", "landscape-removal", "home-surface-protection", "remodeling-floor-protection", "tile-demolition"],
 "map": "Nexus North, Gallatin, TN",
 "nearby": ["nexus-south", "dobbins-pike", "airport-road"]
},
{
 "slug": "nexus-south", "name": "Nexus South",
 "title": "Junk Removal & Clean-Outs in Nexus South, Gallatin TN",
 "desc": "Downsizing clean-outs, appliance removal, junk hauling and remodel protection for the Nexus South 55+ community in Gallatin, TN. Courteous, careful crews.",
 "lead": "Courteous, careful help for Nexus South homeowners: downsizing clean-outs, furniture and appliance removal, and remodel updates without the hassle.",
 "about": [
  "Nexus South is a newer, gated 55+ community in Gallatin with resort-style amenities. Many residents are moving in from larger homes, which often means more furniture, boxes and belongings than the new house can hold, plus updates to make a new home feel like their own.",
  "We help Nexus South residents with downsizing and move-in clean-outs, removing furniture and appliances that no longer fit, hauling away moving boxes, and clearing out garages. We do the heavy lifting so you don't have to, donate usable furniture whenever possible, and protect floors and door frames on the way out. For remodel projects we offer dust, floor and surface protection so you can stay comfortably in your home while work is done. We coordinate gate access and arrival times ahead of every visit."
 ],
 "jobs": ["junk-removal", "appliance-removal", "garage-clean-out", "remodeling-plastic-protection", "home-surface-protection", "bathroom-demolition"],
 "map": "Nexus South, Gallatin, TN",
 "nearby": ["nexus-north", "fairvue-plantation", "station-camp"]
},
{
 "slug": "kennesaw-farms", "name": "Kennesaw Farms",
 "title": "Demolition & Junk Removal in Kennesaw Farms, Gallatin TN",
 "desc": "Kitchen and bath demolition, deck and fence removal and junk hauling for Kennesaw Farms homes in Gallatin, TN. Clean, careful crews. Free quotes.",
 "lead": "Established family homes ready for updates. Kitchen and bath tear-outs, deck and fence replacements and clean-outs in Kennesaw Farms.",
 "about": [
  "Kennesaw Farms is one of Gallatin's popular established neighborhoods. Many homes have reached the age where original kitchens, bathrooms, decks and fences are due for replacement, and families are updating to fit how they live today.",
  "We regularly help Kennesaw Farms homeowners with kitchen and bathroom demolition ahead of remodels, deck removal before new decks or patios go in, fence removal (posts and footings included), and clearing out garages and attics. Inside the home, we set up dust barriers and floor protection so the rest of the house stays livable during the project."
 ],
 "jobs": ["kitchen-demolition", "bathroom-demolition", "deck-removal", "fence-removal", "garage-clean-out", "remodeling-plastic-protection"],
 "map": "Kennesaw Farms, Gallatin, TN",
 "nearby": ["downtown-gallatin", "station-camp", "fairvue-plantation"]
},
{
 "slug": "station-camp", "name": "Station Camp",
 "title": "Demolition & Junk Removal in Station Camp, Gallatin TN",
 "desc": "Demolition, junk removal and clean-outs for the Station Camp area of Gallatin, TN. Basements, decks, sheds, fencing and remodel tear-outs. Free quotes.",
 "lead": "Subdivisions and country lots around Station Camp Creek. Remodel tear-outs, outdoor demolition and hauling for busy families.",
 "about": [
  "The Station Camp area, on the west side of Gallatin around Station Camp Creek and the Station Camp schools, combines family subdivisions with more rural properties. That mix means our work here ranges from basement and bonus-room tear-outs to old sheds, fences and outbuildings on larger lots.",
  "Station Camp homeowners call us for interior demolition before remodels, finished basement tear-outs after water damage, deck and shed removal, fence removal, and junk hauling for busy households. We schedule around school drop-off and pick-up traffic when we can, keep the driveway clear, and leave the property clean at the end of every day."
 ],
 "jobs": ["large-room-demolition", "drywall-removal", "deck-removal", "shed-removal", "fence-removal", "junk-removal"],
 "map": "Upper Station Camp Creek Rd, Gallatin, TN",
 "nearby": ["fairvue-plantation", "kennesaw-farms", "dobbins-pike"]
},
]
