# Nearby town pages at /service-areas/<slug>/. Like the Gallatin area pages, each needs its own
# unique text and FAQs. Pages that only swap the town name get treated as "doorway pages" and hurt rankings.
# Fields: slug, name, title, desc, lead, about[], jobs[service slugs], map (Google Maps search text),
#         nearby[town slugs, or "gallatin" for the Gallatin service areas page], faqs[(q, a)]

TOWNS = [
{
 "slug": "hendersonville-tn", "name": "Hendersonville",
 "title": "Demolition & Junk Removal in Hendersonville, TN | Free Quotes",
 "desc": "Demolition, junk removal and remodel protection in Hendersonville, TN. Decks, sheds, kitchens, baths, concrete and clean-outs. Free quotes.",
 "lead": "Sumner County's largest city, served by a local crew from just up the road in Gallatin. Deck and shed removal, remodel tear-outs, concrete and junk hauling.",
 "about": [
  "Hendersonville is the largest city in Sumner County, with homes spread from the Indian Lake Peninsula and the Old Hickory Lake shoreline to Drakes Creek and the neighborhoods off Main Street and Indian Lake Boulevard. Much of the city grew up after Old Hickory Dam created the lake in the 1950s, and plenty of those homes are now due for kitchen, bathroom and outdoor updates.",
  "Around the lake, we do a lot of deck and patio removal for new outdoor living spaces, shed and playset tear-downs, and concrete removal ahead of new driveways and patios. Inside, we handle kitchen and bathroom demolition before remodels, with floor and dust protection so the rest of the house stays clean. We also haul away the junk that piles up in garages and attics, often the same or next day. Many Hendersonville neighborhoods have HOAs, so we follow their rules on work hours, parking and trailers."
 ],
 "jobs": ["deck-removal", "shed-removal", "kitchen-demolition", "bathroom-demolition", "concrete-removal", "junk-removal"],
 "map": "Hendersonville, TN",
 "nearby": ["gallatin", "goodlettsville-tn", "white-house-tn"],
 "faqs": [
  ("Do you charge extra to come to Hendersonville?", "No. Hendersonville is part of our regular service area, just down the road from our Gallatin base, so there's no travel fee. Your quote covers labor, hauling and disposal."),
  ("Can you remove a deck or patio on a lakefront home?", "Yes. We remove decks, stairs and patios on lakefront and lake-view properties. Work on structures at the water's edge on Old Hickory Lake may need approval from the U.S. Army Corps of Engineers, which manages the shoreline, so check that first and we'll plan the job around it."),
  ("Do I need a permit for demolition in Hendersonville?", "It depends on the job. Interior tear-outs for a remodel are often covered by your contractor's building permit, while removing a whole structure may need a demolition permit from the City of Hendersonville. We'll help you figure out what your project needs before we start."),
 ],
},
{
 "slug": "portland-tn", "name": "Portland",
 "title": "Demolition & Junk Removal in Portland, TN | Free Quotes",
 "desc": "Shed, fence and concrete removal, junk hauling and remodel demolition in Portland, TN. Local, veteran-owned crew from nearby Gallatin. Free quotes.",
 "lead": "From older homes near downtown to farms and larger lots at the edge of town. Shed and fence removal, concrete breakout, clean-outs and junk hauling in Portland.",
 "about": [
  "Portland sits in the northern part of Sumner County near the Kentucky line, with part of the city reaching into Robertson County. It's known for the Middle Tennessee Strawberry Festival every spring, and for a mix of established neighborhoods, newer subdivisions and rural properties with plenty of room to spread out.",
  "That mix keeps our Portland jobs varied: old sheds, carports and long fence lines on bigger lots, concrete pads and walkways, estate and garage clean-outs, and interior demolition when an older house gets a new kitchen or bathroom. For country properties we bring a trailer sized for the job and plan the haul so there are no wasted trips. For barns and large outbuildings, we'll point you to a trusted partner."
 ],
 "jobs": ["shed-removal", "fence-removal", "concrete-removal", "garage-clean-out", "junk-removal", "interior-demolition"],
 "map": "Portland, TN",
 "nearby": ["gallatin", "white-house-tn", "hendersonville-tn"],
 "faqs": [
  ("Do you serve the Robertson County side of Portland?", "Yes. We serve all of Portland, on both the Sumner County and Robertson County sides, plus the surrounding rural areas."),
  ("Can you take down an old barn on my property?", "We focus on sheds, carports, fences and smaller outbuildings. For barns and other large structures, we can refer you to a trusted demolition partner."),
  ("How fast can you pick up junk in Portland?", "We're open 24/7 and based in nearby Gallatin, so junk pickups in Portland can often be scheduled within a day or two. Send a few photos for a quick price."),
 ],
},
{
 "slug": "white-house-tn", "name": "White House",
 "title": "Demolition & Junk Removal in White House, TN | Free Quotes",
 "desc": "Junk removal, deck and fence removal, remodel demolition and floor protection in White House, TN. Veteran-owned local crew. Free quotes.",
 "lead": "A fast-growing town with brand-new subdivisions and long-standing homes alike. Move-in junk removal, deck and fence tear-outs, remodel demolition and remodel protection.",
 "about": [
  "White House sits along I-65 where Highway 76 meets US 31W, straddling the line between Sumner and Robertson counties. The town has grown quickly, with new subdivisions going up next to homes that have been there for decades.",
  "In newer neighborhoods we often haul away move-in boxes and builder leftovers, remove builder-grade landscaping and fencing, and protect brand-new floors and finishes when owners start upgrading. In older homes we handle kitchen and bathroom demolition, drywall removal and garage clean-outs. Wherever you are in White House, we quote upfront and leave the site swept clean."
 ],
 "jobs": ["junk-removal", "fence-removal", "deck-removal", "kitchen-demolition", "remodeling-floor-protection", "garage-clean-out"],
 "map": "White House, TN",
 "nearby": ["gallatin", "portland-tn", "goodlettsville-tn"],
 "faqs": [
  ("Do you work on both the Sumner and Robertson County sides of White House?", "Yes. We serve all of White House, whichever county your home is in."),
  ("Can you protect new floors while my contractor works?", "Yes. Our floor, surface and dust protection keeps new hardwood, LVP, tile and countertops safe during a remodel, even when we're not the ones doing the demolition."),
  ("Do you haul away moving boxes and leftover building materials?", "Yes. Move-in clean-ups are common jobs for us in newer White House neighborhoods. We load everything and recycle the cardboard whenever possible."),
 ],
},
{
 "slug": "goodlettsville-tn", "name": "Goodlettsville",
 "title": "Demolition & Junk Removal in Goodlettsville, TN | Free Quotes",
 "desc": "Interior demolition, junk removal, clean-outs and concrete removal in Goodlettsville, TN. Homes, rentals and businesses. Free quotes.",
 "lead": "Homes, rentals and small businesses on both sides of the county line. Interior tear-outs, estate and garage clean-outs, concrete removal and junk hauling.",
 "about": [
  "Goodlettsville straddles the Davidson and Sumner county line just north of Nashville along I-65. It mixes historic areas near Main Street and Moss-Wright Park, home to the reconstructed Mansker's Station fort, with established neighborhoods, newer subdivisions and busy commercial corridors like Long Hollow Pike.",
  "Many Goodlettsville homes are a few decades old, so we do a lot of interior demolition for kitchen and bath remodels, drywall removal after leaks, and estate, garage and attic clean-outs. For rental owners and businesses, we handle unit turnovers, office and retail strip-outs and junk hauling, and we schedule around tenants and business hours."
 ],
 "jobs": ["interior-demolition", "drywall-removal", "junk-removal", "attic-clean-out", "concrete-removal", "large-room-demolition"],
 "map": "Goodlettsville, TN",
 "nearby": ["hendersonville-tn", "white-house-tn", "gallatin"],
 "faqs": [
  ("Do you serve the Davidson County side of Goodlettsville?", "Yes. We serve all of Goodlettsville, on both the Davidson County and Sumner County sides."),
  ("Can you clean out a rental between tenants?", "Yes. We remove leftover furniture, junk and damaged materials, and can tear out flooring or drywall so your rental is ready for repairs."),
  ("Do you do commercial interior demolition?", "Yes, for small commercial spaces like offices and retail suites. We remove non-load-bearing walls, ceilings, flooring and fixtures, haul everything away, and work around your business hours."),
 ],
},
]
