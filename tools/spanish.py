# Spanish pages (/es/). Plain text only; the builder escapes it.
# Nobody on the team speaks Spanish yet, so these pages invite people to TEXT us
# and never say "Hablamos español". Change that wording only once it's true.

# English page -> Spanish page (used for the language switch and hreflang tags)
ES_PATHS = {
    "/": "/es/",
    "/services/": "/es/servicios/",
    "/junk-removal/": "/es/retiro-de-basura/",
    "/interior-demolition/": "/es/demolicion-interior/",
    "/kitchen-demolition/": "/es/demolicion-de-cocinas/",
    "/bathroom-demolition/": "/es/demolicion-de-banos/",
    "/shed-removal/": "/es/demolicion-de-cobertizos/",
    "/concrete-removal/": "/es/remocion-de-concreto/",
    "/thank-you/": "/es/gracias/",
    "/privacy-policy/": "/es/politica-de-privacidad/",
}

CATEGORIES_ES = {
    "demolition": ("Demolición", "Demolición interior y exterior, desde un solo cobertizo hasta una demolición interior completa."),
    "cleanout": ("Retiro de Basura y Limpiezas", "Nosotros cargamos y acarreamos todo, y donamos y reciclamos siempre que podemos."),
    "protection": ("Protección para Remodelaciones", "Protección de pisos, superficies, encintado y polvo para que su remodelación quede limpia."),
}

# Spanish name and one-line description for every service (English slug -> text)
SERVICE_NAMES_ES = {
    "shed-removal": ("Demolición de Cobertizos", "Derribamos cobertizos de madera, metal y vinil, quitamos pisos y bases, y nos llevamos todo."),
    "deck-removal": ("Remoción de Terrazas", "Quitamos terrazas (decks) viejas, escaleras y bases, y nos llevamos todos los escombros."),
    "fence-removal": ("Remoción de Cercas", "Quitamos cercas de madera, malla ciclónica y paneles dañados, con postes y bases de concreto incluidos."),
    "garage-demolition": ("Demolición Interior de Garajes", "Quitamos tablaroca, repisas, gabinetes, bancos de trabajo y aislamiento del interior del garaje."),
    "concrete-removal": ("Remoción de Concreto", "Rompemos y retiramos entradas de auto, patios, banquetas y losas, y llevamos el concreto a reciclar."),
    "landscape-removal": ("Remoción de Jardinería", "Quitamos arbustos, plantas, piedra decorativa y durmientes para que empiece de nuevo."),
    "exterior-demolition": ("Demolición Exterior", "Porches, escalones, revestimiento, toldos, cocheras pequeñas, pérgolas y juegos infantiles."),
    "interior-demolition": ("Demolición Interior", "Demolemos cuartos hasta los montantes o quitamos solo lo necesario, con control de polvo."),
    "kitchen-demolition": ("Demolición de Cocinas", "Quitamos gabinetes, encimeras, azulejo, pisos y electrodomésticos para su remodelación."),
    "bathroom-demolition": ("Demolición de Baños", "Tinas, regaderas, azulejo, lavabos e inodoros fuera, hasta los montantes."),
    "living-room-demolition": ("Demolición de Salas", "Quitamos pisos, paneles, muebles empotrados, chimeneas decorativas y tablaroca."),
    "large-room-demolition": ("Demolición de Espacios Grandes", "Sótanos, cuartos adicionales, espacios abiertos y locales comerciales pequeños."),
    "drywall-removal": ("Remoción de Tablaroca", "Quitamos tablaroca (drywall) y techos dañados por agua o para remodelar, con control de polvo."),
    "tile-demolition": ("Demolición de Azulejo", "Quitamos azulejo de pisos, paredes y regaderas, incluido el mortero, y dejamos la superficie plana."),
    "junk-removal": ("Retiro de Basura", "Muebles, colchones, electrodomésticos, desechos de jardín y escombros, muchas veces el mismo día."),
    "appliance-removal": ("Retiro de Electrodomésticos", "Refrigeradores, lavadoras, secadoras, estufas, calentadores de agua y aires acondicionados."),
    "garage-clean-out": ("Limpieza de Garajes", "Sacamos años de cosas acumuladas, muebles viejos y repisas para que vuelva a usar su garaje."),
    "attic-clean-out": ("Limpieza de Áticos", "Bajamos cajas, muebles viejos y escombros de áticos estrechos y calientes, sin dañar sus techos."),
    "crawlspace-clean-out": ("Limpieza Bajo la Casa", "Quitamos barrera de vapor vieja, aislamiento caído, escombros y basura del espacio bajo la casa (crawlspace)."),
    "remodeling-floor-protection": ("Protección de Pisos", "Protegemos madera, azulejo, vinil y alfombra contra rayones, golpes, derrames y polvo durante su remodelación."),
    "remodeling-tape-off": ("Encintado para Remodelaciones", "Enmascaramos molduras, gabinetes, ventanas, contactos y superficies antes de pintar o demoler."),
    "remodeling-plastic-protection": ("Barreras de Plástico contra el Polvo", "Paredes de plástico de piso a techo, puertas con cierre y rejillas selladas para contener el polvo."),
    "home-surface-protection": ("Protección de Superficies", "Protegemos encimeras, gabinetes, marcos de puertas, barandales, ventanas y electrodomésticos."),
}

# Full Spanish service pages (English slug -> page). "related" uses English slugs.
SERVICES_ES = {
"junk-removal": {
 "title": "Retiro de Basura en Gallatin, TN | Recogida el Mismo Día",
 "desc": "Retiro de basura en Gallatin, TN. Muebles, colchones, electrodomésticos, desechos de jardín y escombros de construcción. Recogida el mismo día.",
 "lead": "Usted nos señala y nosotros cargamos. Muebles, colchones, electrodomésticos, desechos de jardín, escombros de construcción y más, retirados muchas veces el mismo día.",
 "intro": [
  "Ya sea un sofá viejo, un garaje lleno de cosas o lo que quedó de una remodelación, retirar la basura debe ser fácil. No tiene que arrastrar nada hasta la calle, rentar un camión ni hacer viajes al basurero. Nuestro equipo hace todo el trabajo de cargar desde donde estén las cosas en su casa o propiedad.",
  "Siempre que es posible, donamos muebles y artículos del hogar en buen estado a organizaciones locales, reciclamos metal, aparatos electrónicos y cartón, y solo llevamos al relleno sanitario lo que no se puede reutilizar. Nuestra meta es mantener fuera del relleno sanitario del condado de Sumner todo lo que podamos."
 ],
 "included": ["Todo el trabajo de levantar, cargar y subir al tráiler desde cualquier parte de su propiedad", "Muebles, colchones y bases de cama", "Electrodomésticos, aparatos electrónicos y equipo de ejercicio", "Desechos de jardín, ramas y escombros de tormentas", "Escombros de construcción y remodelación", "Jacuzzis, juegos infantiles y trampolines", "Barrido del área después de retirar todo"],
 "steps": [
  ("Pida una cotización", "Use el formulario o envíenos un mensaje de texto con una descripción o fotos. Le podemos dar un rango de precio desde el principio y confirmarlo en el lugar."),
  ("Programe", "Escoja el horario que le convenga. En Gallatin muchas veces hay recogidas el mismo día o el día siguiente."),
  ("Precio en el lugar", "Al llegar, revisamos todo y confirmamos el precio antes de levantar cualquier cosa. Sin compromiso."),
  ("Cargamos todo", "Nuestro equipo saca todo lo que usted quiere retirar, ya sea del sótano, el ático, el segundo piso o el patio."),
  ("Disposición responsable", "Separamos las cosas para donar, reciclar y desechar. Barremos antes de irnos.")
 ],
 "prep": ["Haga una lista o marque lo que se va (las notas adhesivas funcionan muy bien)", "Aparte lo que se va a quedar para que no haya confusión", "Asegúrese de que podamos estacionarnos cerca de la casa o la entrada", "Retire materiales peligrosos como pintura, químicos y combustible, que no podemos llevarnos"],
 "cost": "El retiro de basura se cotiza según el espacio que ocupan sus cosas en nuestro tráiler, desde un solo artículo hasta una carga completa. Los materiales muy pesados como concreto, tierra, tejas o azulejo se cotizan por peso. La mano de obra, la carga y la disposición están incluidas en el precio que le damos.",
 "faqs": [
  ("¿Qué es lo que no se pueden llevar?", "No podemos llevarnos materiales peligrosos como pintura, químicos, solventes, combustible, aceite de motor, asbesto, desechos médicos o tanques de propano. El condado de Sumner organiza eventos de recolección de desechos peligrosos del hogar para estos materiales."),
  ("¿Tengo que estar en casa?", "Es mejor que esté presente para confirmar las cosas y el precio. Para recogidas en la acera o en el exterior, muchas veces podemos coordinar con usted por mensaje de texto y fotos."),
  ("¿Donan las cosas?", "Sí. Los muebles y artículos del hogar en buen estado van a centros de donación locales siempre que sea posible.")
 ],
 "related": ["shed-removal", "concrete-removal", "interior-demolition"]
},
"interior-demolition": {
 "title": "Demolición Interior en Gallatin, TN | Para Remodelaciones",
 "desc": "Demolición interior en Gallatin, TN. Cocinas, baños, tablaroca, pisos y paredes no estructurales retirados con control de polvo para su remodelación.",
 "lead": "¿Va a remodelar? Demolemos cuartos hasta los montantes o quitamos solo lo que necesita, con control de polvo y un trabajo limpio y cuidadoso dentro de su casa.",
 "intro": [
  "La demolición interior (también llamada vaciado o demolición selectiva) es la primera etapa de casi cualquier remodelación. Bien hecha, le ahorra tiempo a su contratista, mantiene limpio el resto de su casa y deja ver problemas ocultos como daños por agua, madera podrida o cableado viejo antes de que empiece el trabajo nuevo.",
  "Hacemos vaciados completos y demoliciones selectivas: cocinas, baños, salas, sótanos, tablaroca y yeso, techos, pisos, azulejo, gabinetes, molduras y paredes no estructurales. Aislamos el área de trabajo, protegemos sus pisos y sacamos todos los escombros de la casa el mismo día."
 ],
 "included": ["Protección de pisos y barreras de plástico contra el polvo antes de empezar", "Retiro de gabinetes, encimeras, accesorios y molduras", "Retiro de tablaroca, yeso y techos", "Retiro de pisos, alfombra, azulejo y bases de piso", "Retiro de paredes no estructurales", "Retiro diario de escombros, sin necesidad de contenedor en la mayoría de los casos", "Área de trabajo barrida y aspirada al final de cada día"],
 "steps": [
  ("Recorrido del proyecto", "Recorremos el espacio con usted y con su contratista (si tiene uno) y marcamos exactamente qué se quita y qué se queda. Lo que se va a conservar se etiqueta."),
  ("Protección", "Cubrimos los pisos en nuestro camino, aislamos el área de trabajo con barreras de plástico, cubrimos las rejillas del aire y protegemos las puertas."),
  ("Seguridad de servicios", "Antes de abrir cualquier pared, un plomero o electricista con licencia corta o confirma que el agua y la electricidad del área están seguras."),
  ("Demolición", "Retiramos los materiales en orden: accesorios, gabinetes y molduras, y después paredes, techos y pisos. Los escombros se embolsan y se sacan de forma continua."),
  ("Acabado limpio", "Quitamos clavos y grapas de los montantes y el subpiso, barremos y aspiramos, y el espacio queda listo para su contratista.")
 ],
 "prep": ["Saque sus cosas personales del área de trabajo y de los cuartos cercanos", "Decida qué quiere conservar, como gabinetes, puertas o accesorios", "Si hay que desconectar accesorios, programe a un plomero o electricista", "Planee dónde estarán su familia y sus mascotas, lejos del área de trabajo"],
 "cost": "El precio de una demolición interior depende de los pies cuadrados, cuántas capas de material hay (las casas viejas muchas veces tienen piso sobre piso), qué se va a retirar, la cantidad de escaleras o la distancia hasta la salida, y cuánta protección necesita el resto de la casa. Le damos un alcance detallado y un precio antes de empezar.",
 "faqs": [
  ("¿Pueden saber si una pared es estructural?", "Le avisamos si una pared parece estructural, pero un contratista o ingeniero debe confirmarlo. Solo quitamos paredes que se haya confirmado que no son estructurales."),
  ("¿Y el asbesto en casas viejas?", "Las casas construidas antes de 1980, más o menos, pueden tener asbesto en los pisos, en la pasta de la tablaroca o en los techos con textura (popcorn). Recomendamos hacer una prueba antes de demoler. No hacemos remoción de asbesto y detenemos el trabajo si sospechamos que hay."),
  ("¿Se va a llenar de polvo mi casa?", "Usamos barreras de plástico, protección de pisos y rejillas cubiertas para mantener el polvo dentro del área de trabajo.")
 ],
 "related": ["kitchen-demolition", "bathroom-demolition", "remodeling-plastic-protection"]
},
"kitchen-demolition": {
 "title": "Demolición de Cocinas en Gallatin, TN | Gabinetes y Encimeras",
 "desc": "Demolición de cocinas en Gallatin, TN. Retiramos gabinetes, encimeras, azulejo, pisos, electrodomésticos y tablaroca con cuidado para su remodelación.",
 "lead": "¿Va a remodelar su cocina? Quitamos gabinetes, encimeras, azulejo, pisos y electrodomésticos, y le dejamos a su contratista un cuarto limpio y despejado.",
 "intro": [
  "Demoler una cocina es más complicado de lo que parece. Hay conexiones de agua y gas, encimeras pesadas de piedra o laminado, gabinetes superiores anclados a los montantes, azulejo pegado a la tablaroca y muchas veces varias capas de piso. Retirar todo con cuidado protege el resto de su casa y le da a su contratista un buen comienzo.",
  "Podemos hacer un vaciado completo hasta los montantes y el subpiso, o una demolición selectiva; por ejemplo, conservar los gabinetes y quitar solo las encimeras y el azulejo. Si quiere donar sus gabinetes o electrodomésticos viejos, los retiramos con cuidado para que sigan sirviendo."
 ],
 "included": ["Desconexión de electrodomésticos (por un profesional con licencia cuando hay gas o cableado directo) y retiro", "Retiro de encimeras: granito, cuarzo, laminado, azulejo y madera", "Retiro de gabinetes superiores e inferiores, con cuidado para reutilizarlos si lo pide", "Retiro del azulejo de la pared (backsplash) y de la tablaroca", "Retiro de pisos hasta el subpiso", "Retiro de plafones, cajones de techo y despensas", "Retiro completo de escombros y limpieza final"],
 "steps": [
  ("Planear el alcance", "Confirmamos exactamente qué se quita, qué se queda y si algo se va a conservar o donar."),
  ("Cortes de servicio", "Se cierran y tapan las líneas de agua, y un profesional con licencia desconecta los electrodomésticos de gas o con cableado directo. Confirmamos que todo esté seguro antes de empezar."),
  ("Protección", "Protegemos los pisos desde la cocina hasta la salida, colgamos barreras de plástico hacia los cuartos de al lado y cubrimos las rejillas del aire."),
  ("Demolición", "Primero los electrodomésticos, luego las encimeras, los gabinetes superiores, los inferiores, el azulejo, los plafones y el piso, en ese orden, para que el cuarto sea seguro."),
  ("Acarreo y limpieza", "Sacamos los escombros mientras trabajamos. La cocina queda barrida, aspirada y lista para el siguiente oficio.")
 ],
 "prep": ["Vacíe todos los gabinetes, cajones y la despensa", "Prepare una cocina temporal en otro cuarto", "Desconecte los aparatos pequeños y despeje las encimeras", "Coordine el calendario con su contratista, plomero y electricista"],
 "cost": "El precio de una demolición de cocina depende del tamaño de la cocina, la cantidad de gabinetes, el material de las encimeras (la piedra es pesada y se maneja con cuidado), cuánto azulejo hay, las capas de piso, si se van a conservar cosas y la distancia hasta la salida. La mayoría de las demoliciones de cocina se terminan en uno o dos días.",
 "faqs": [
  ("¿Pueden conservar mis gabinetes para donarlos?", "Sí. Si están en buen estado, los quitamos con cuidado y podemos llevarlos a un centro de donación local o dejárselos a usted."),
  ("¿Ustedes desconectan la estufa de gas?", "Las líneas de gas debe desconectarlas y taparlas un plomero o técnico de gas con licencia. Nosotros retiramos el aparato cuando ya está desconectado de forma segura."),
  ("¿Cuánto tiempo estaré sin cocina?", "La demolición en sí normalmente toma uno o dos días. El tiempo total de su remodelación depende de su contratista.")
 ],
 "related": ["interior-demolition", "bathroom-demolition", "junk-removal"]
},
"bathroom-demolition": {
 "title": "Demolición de Baños en Gallatin, TN | Tinas, Regaderas y Azulejo",
 "desc": "Demolición de baños en Gallatin, TN. Retiramos tinas, regaderas, azulejo, lavabos, inodoros y tablaroca hasta los montantes para su remodelación.",
 "lead": "Tinas, regaderas, azulejo, lavabos e inodoros fuera, hasta los montantes. Una demolición de baño limpia y cuidadosa para que su remodelación empiece bien.",
 "intro": [
  "Demoler un baño es uno de los trabajos interiores más difíciles. Una tina de hierro fundido puede pesar 300 libras o más, el azulejo muchas veces está sobre una capa gruesa de mortero, y los baños son espacios pequeños donde el resto de la casa está a solo una puerta de distancia. También es donde más se encuentran daños ocultos por agua y madera podrida.",
  "Retiramos desde un simple cambio de lavabo e inodoro hasta un vaciado completo: tinas (incluidas las de hierro fundido), regaderas de fibra de vidrio y de azulejo, bases de regadera, pisos y paredes de azulejo, muebles de baño, inodoros, espejos, botiquines, extractores, tablaroca y el subpiso cuando hace falta."
 ],
 "included": ["Cierre del agua y tapado de las líneas", "Retiro de inodoro, lavabo, mueble de baño y espejo", "Retiro de la tina, incluso rompiendo en el lugar las tinas de hierro fundido cuando es necesario", "Retiro de paredes de regadera, azulejo y base de regadera", "Retiro de piso de azulejo y capa de mortero", "Retiro de tablaroca, tablero de cemento y subpiso dañado", "Retiro de escombros y un baño limpio y aspirado"],
 "steps": [
  ("Alcance", "Confirmamos qué se quita y buscamos señales de daño por agua. Le diremos lo que encontremos al abrir paredes y pisos."),
  ("Protección", "Cubrimos los pisos desde el baño hasta la salida, sellamos la puerta con una barrera de polvo con cierre y cubrimos las rejillas del aire."),
  ("Fuera los accesorios", "Cerramos el agua y tapamos las líneas. Primero salen el inodoro, el lavabo y los accesorios, y tapamos el drenaje para bloquear gases y escombros."),
  ("Tina, regadera y azulejo", "Quitamos el azulejo y el tablero de respaldo, y después la tina o la regadera. Las tinas pesadas de hierro fundido a veces se rompen en pedazos para sacarlas de forma segura."),
  ("Limpio y listo", "Sacamos los escombros, limpiamos los montantes y el subpiso de clavos y restos de azulejo, y le mostramos cualquier daño a usted y a su contratista.")
 ],
 "prep": ["Saque toallas, artículos de baño, tapetes y todo lo que guarde en el baño", "Planee que su familia use otro baño", "Díganos dónde está la llave principal del agua", "Coordine los tiempos con su plomero y su contratista"],
 "cost": "El precio de una demolición de baño depende del tamaño del baño, el tipo de tina (la de hierro fundido requiere más trabajo), cuánto azulejo hay y si está sobre mortero, la cantidad de accesorios, el subpiso dañado y la distancia para sacar los escombros de la casa. La mayoría de los baños se terminan en un día.",
 "faqs": [
  ("¿Pueden quitar una tina de hierro fundido?", "Sí. La sacamos entera o la rompemos en pedazos en el lugar, según el espacio y lo que usted prefiera."),
  ("¿Qué pasa si encuentran daño por agua o moho?", "Nos detenemos y se lo mostramos. Las áreas pequeñas de subpiso o tablaroca dañados normalmente se pueden retirar como parte del trabajo. Los problemas grandes de moho los debe atender un especialista en remediación."),
  ("¿Pueden quitar solo el azulejo y dejar la tina?", "Sí. La demolición selectiva es común, y protegemos la tina mientras trabajamos.")
 ],
 "related": ["kitchen-demolition", "interior-demolition", "tile-demolition"]
},
"shed-removal": {
 "title": "Demolición de Cobertizos en Gallatin, TN | Cotización Gratis",
 "desc": "Demolición de cobertizos en Gallatin, TN. Cobertizos de madera, metal y vinil derribados, pisos y bases retirados, y nos llevamos todo. Cotización gratis.",
 "lead": "¿Tiene un cobertizo viejo, podrido o que ya no quiere? Lo derribamos, quitamos el piso y la base, nos llevamos cada tabla y dejamos el terreno listo para lo que siga.",
 "intro": [
  "Los cobertizos son de los trabajos más comunes que hacemos en Gallatin. Años de humedad de Tennessee, termitas y tormentas dañan los cobertizos de madera, y los de metal se oxidan en las uniones. Cuando un cobertizo empieza a inclinarse, a gotear o a llenarse de animales, quitarlo casi siempre es más barato y seguro que repararlo.",
  "Trabajamos con cobertizos de todo tipo y tamaño: cobertizos pequeños de jardín, bodegas de 10x12 y 12x16, techados adosados, cobertizos de kit y de metal. Para graneros y construcciones grandes, lo referimos con un socio de confianza. Si el cobertizo todavía está lleno, podemos vaciarlo primero y llevarnos todo en el mismo viaje."
 ],
 "included": ["Vaciar el cobertizo de lo que tenga guardado (si hace falta)", "Desconexión de cableado sencillo por un electricista con licencia cuando se requiere", "Demolición de paredes, techo, puertas y ventanas", "Retiro del piso de madera, patines o soportes", "Romper una losa de concreto o base de grava (opcional)", "Llevar todos los escombros a disposición o reciclaje adecuados", "Rastrillar el área y recoger clavos con un barredor magnético"],
 "steps": [
  ("Cotización gratis", "Mándenos una o dos fotos por el formulario o por mensaje de texto, o vamos a verlo. Le preguntaremos el tamaño, de qué está hecho, qué tiene adentro y qué hay debajo."),
  ("Programación", "La mayoría de las demoliciones de cobertizos se programan en pocos días. Si el cobertizo tiene electricidad, hay que desconectarla antes de empezar, y le avisaremos si es el caso."),
  ("Demolición", "Primero quitamos el techo, después las paredes y la estructura, de arriba hacia abajo para que nada se caiga de forma inesperada. La mayoría de los cobertizos estándar toman de dos a cuatro horas."),
  ("Piso y base", "Levantamos el piso, los patines y los bloques. Si hay una losa de concreto y quiere quitarla, también la rompemos y la retiramos."),
  ("Limpieza", "Cargamos y nos llevamos todo. Rastrillamos el área y pasamos un barredor magnético para recoger clavos y tornillos sueltos, para que el patio sea seguro para niños, mascotas y podadoras.")
 ],
 "prep": ["Saque del cobertizo lo que quiera conservar, o díganos qué guardar", "Avísenos si el cobertizo tiene electricidad o agua", "Si es posible, despeje un camino del cobertizo a la entrada o la calle", "Avise a su asociación de vecinos (HOA) si su vecindario pide aviso para trabajos exteriores"],
 "cost": "El precio depende del tamaño del cobertizo, de qué está hecho, si tiene losa de concreto, qué tan lleno está y qué tan cerca podemos estacionar nuestro tráiler. Un cobertizo pequeño y vacío de madera junto a la entrada cuesta mucho menos que uno grande al fondo de un patio cercado con losa debajo. Le damos un precio firme antes de empezar.",
 "faqs": [
  ("¿Necesito un permiso para quitar un cobertizo en Gallatin?", "La mayoría de las construcciones pequeñas sin servicios no necesitan permiso de demolición, pero las reglas cambian. Si el cobertizo tiene electricidad o es grande, le ayudamos a consultar primero con el Departamento de Códigos de la Ciudad de Gallatin."),
  ("¿Pueden quitar un cobertizo que ya se cayó?", "Sí. Los cobertizos caídos o dañados por tormentas son trabajos comunes. Solo separamos los escombros y nos los llevamos."),
  ("¿También se pueden llevar la losa de concreto?", "Sí. Quitar la losa es un servicio adicional. Díganos y lo incluimos en su cotización.")
 ],
 "related": ["concrete-removal", "junk-removal", "fence-removal"]
},
"concrete-removal": {
 "title": "Remoción de Concreto en Gallatin, TN | Entradas, Patios y Losas",
 "desc": "Remoción de concreto en Gallatin, TN. Rompemos y retiramos entradas de auto, patios, banquetas, losas y escalones, y llevamos el concreto a reciclar.",
 "lead": "¿Entrada de auto agrietada, patio hundido o losa vieja? La rompemos, la llevamos a reciclar y dejamos el área lista para concreto nuevo, adoquines o pasto.",
 "intro": [
  "En el centro de Tennessee el concreto se agrieta, se levanta y se hunde con el tiempo por el suelo arcilloso y los ciclos de congelación y deshielo. Cuando las grietas se abren o las losas se inclinan y se vuelven un peligro para tropezar, la solución es quitarlas y reemplazarlas, y quitarlas es un trabajo pesado y polvoso que necesita las herramientas correctas.",
  "Quitamos entradas de auto, patios, banquetas, losas de cobertizos y garajes, escalones de porche, pisos alrededor de albercas, bases y muros de contención pequeños. Rompemos el concreto en pedazos manejables, lo cargamos y lo llevamos a un reciclador, donde se tritura y se reutiliza como material de base siempre que es posible."
 ],
 "included": ["Corte con sierra para dejar una orilla limpia cuando solo se quita parte de la losa", "Romper el concreto con martillos neumáticos o rompedores de maquinaria", "Cortar y retirar varilla y malla de alambre", "Cargar y llevar todo el concreto a un reciclador", "Retiro de la base de grava si lo pide", "Nivelación básica del área después de quitar el concreto", "Barrido y limpieza de las superficies alrededor"],
 "steps": [
  ("Cotización gratis", "Necesitamos el tamaño y el grosor aproximados, si tiene varilla o malla y qué tan cerca puede llegar un camión o tráiler. Las fotos son un gran comienzo."),
  ("Marcar y cortar", "Si vamos a excavar, primero Tennessee 811 marca las líneas de servicio enterradas. Si va a conservar parte de la losa, hacemos un corte recto y limpio con sierra."),
  ("Romper", "Rompemos el concreto en pedazos con martillos neumáticos o rompedores de maquinaria. Protegemos las ventanas, los autos y el revestimiento cercanos de los fragmentos."),
  ("Retiro", "Cargamos y nos llevamos los pedazos. La varilla y la malla se cortan y se reciclan como chatarra."),
  ("Acabado", "Rastrillamos el área y la dejamos con una nivelación básica, lista para su contratista de concreto, adoquines o jardinería.")
 ],
 "prep": ["Mueva los autos, macetas y muebles lejos del concreto", "Avísenos si hay aspersores, luces o drenajes en la losa o cerca de ella", "Díganos qué va a poner después para dejar el nivel correcto", "Cierre las ventanas cercanas, porque romper concreto levanta polvo"],
 "cost": "La remoción de concreto se cotiza principalmente por pies cuadrados y grosor. La varilla o la malla, la distancia para cargar el material, si una máquina puede llegar y las tarifas de disposición también afectan el precio. Una entrada de auto gruesa con varilla requiere mucho más trabajo que una banqueta delgada.",
 "faqs": [
  ("¿Hace mucho ruido y polvo?", "Romper concreto hace ruido. Usamos agua para reducir el polvo cuando es posible y trabajamos en horario normal de día."),
  ("¿Pueden quitar solo una parte de la entrada de auto?", "Sí. Hacemos un corte limpio con sierra para que el concreto que se queda se vea bien y su contratista pueda colar justo hasta ahí."),
  ("¿Qué pasa con el concreto viejo?", "Siempre que es posible, va a un reciclador de concreto, donde se tritura y se convierte en grava de base en lugar de ir al relleno sanitario.")
 ],
 "related": ["shed-removal", "junk-removal", "exterior-demolition"]
},
}

HOME_FAQS_ES = [
    ("¿Cuánto cuesta una demolición en Gallatin, TN?", "El costo depende del tamaño de la estructura, los materiales, el acceso y la eliminación de escombros. Los trabajos pequeños, como un cobertizo o una terraza, cuestan mucho menos que una demolición interior completa. Damos cotizaciones gratis y sin compromiso para que sepa el precio antes de empezar."),
    ("¿Necesito un permiso para demoler una estructura en Gallatin?", "Muchos proyectos de demolición en Gallatin requieren un permiso del Departamento de Códigos de la Ciudad de Gallatin, y los servicios públicos deben desconectarse primero. Le podemos explicar lo que necesita su proyecto."),
    ("¿Qué tipo de basura se llevan?", "Muebles, electrodomésticos, colchones, desechos de jardín, escombros de construcción, jacuzzis, juegos infantiles, cosas acumuladas en garajes, áticos y espacios bajo la casa, y limpiezas completas de casas. No podemos llevarnos materiales peligrosos como pintura, químicos o asbesto."),
    ("¿Protegen mi casa durante una remodelación?", "Sí. Ofrecemos protección de pisos y superficies, encintado profesional y barreras de plástico contra el polvo, ya sea junto con nuestro trabajo de demolición o por separado para el proyecto de su contratista."),
    ("¿Qué tan rápido pueden venir?", "Estamos abiertos las 24 horas, los 365 días del año, y somos de Gallatin, así que muchas veces podemos dar cotizaciones y hacer retiros de basura el mismo día o el día siguiente. Los trabajos de demolición más grandes se programan según los permisos y la desconexión de servicios."),
    ("¿Cómo me comunico con ustedes en español?", "La mejor forma es por mensaje de texto. Escríbanos en español al número de esta página y le responderemos lo antes posible. También puede usar el formulario de cotización."),
    ("¿Donan o reciclan?", "Sí. Donamos artículos útiles siempre que es posible y reciclamos metal, concreto y otros materiales para mantener fuera del relleno sanitario todo lo que podamos."),
]
