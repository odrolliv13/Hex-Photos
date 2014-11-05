from manager import models as pmod

a = pmod.Store()
a.locationName = "Store 1"
a.street = "33rd Street"
a.city = "Auburn"
a.state = "WA"
a.zipcode = "98001"
a.phone = "253.336.4545"
a.active = True
a.save()
b = pmod.Store()
b.locationName = "Store 2"
b.street = "400 N 300 E"
b.city = "Provo"
b.state = "UT"
b.zipcode = "84606"
b.phone = "801.545.5398"
b.active = True
b.save()
c = pmod.Store()
c.locationName = "Store 3"
c.street = "500 North Street"
c.city = "Lehi"
c.state = "UT"
c.zipcode = "84608"
c.phone = "801.242.1234"
c.active = True
c.save()


andres = pmod.User()
andres.username = "andres"
andres.is_active = True
andres.is_staff = True
andres.is_superuser = True
andres.commissionRate = 0.0
andres.save()

andres1 = pmod.User()
andres1.username = "oscar"
andres1.is_active = True
andres1.is_staff = True
andres1.is_superuser = True
andres1.commissionRate = 0.0
andres1.save()

andres2 = pmod.User()
andres2.username = "ben"
andres2.is_active = True
andres2.is_staff = True
andres2.is_superuser = True
andres2.commissionRate = 0.0
andres2.save()


d = pmod.User()
d.password = "password"
d.email = "henry@mail.com"
d.username = d.email
d.first_name = "Henry" 
d.last_name = "Mills"
d.street = "33rd N"
d.city = "Provo"
d.state = "UT"
d.zipcode = "84606"
d.phone = "801.545.6563"
d.is_active = True
d.commissionRate = 0.0
d.save()

ed = pmod.User()
ed.password = "password"
ed.email = "onlinesale@hexphotos.com"
ed.username = ed.email
ed.first_name = "Henry" 
ed.last_name = "Mills"
ed.street = "33rd N"
ed.city = "Provo"
ed.state = "UT"
ed.commissionRate = 0.0
ed.zipcode = "84606"
ed.phone = "801.545.6563"
ed.is_active = True
ed.is_staff = True
ed.save()

e = pmod.User()
e.password = "password"
e.email = "juliahanks@mail.com"
e.username = e.email
e.first_name = "Julia" 
e.last_name = "Hanks"
e.commissionRate = 0.05
e.street = "889 N"
e.city = "Provo"
e.state = "UT"
e.zipcode = "84606"
e.phone = "801.454.8888"
e.is_active = True
e.is_staff = True
e.save()

f = pmod.User()
f.password = "password"
f.email = "peterpetrova@mail.com"
f.username = f.email
f.first_name = "Peter" 
f.last_name = "Petrova"
f.street = "700 East"
f.city = "Provo"
f.state = "UT"
f.zipcode = "84606"
f.phone = "801.333.1232"
f.is_active = True
f.commissionRate = 0.0
f.save()

category3 = pmod.Category()
category3.name = "Cameras"
category3.is_active = True
category3.url = "/shop/catalog/cameras"
category3.imagePath = "base_app/images/nikonj3.jpg"
category3.queryURL = "cameras"
category3.save()

category2 = pmod.Category()
category2.name = "Video Cameras"
category2.is_active = True
category2.url = "/shop/catalog/video_cameras"
category2.imagePath = "base_app/images/videocam.jpg"
category2.queryURL = "video_cameras"
category2.save()

category1 = pmod.Category()
category1.name = "Accessories"
category1.is_active = True
category1.imagePath = "base_app/images/kitnikon.jpg"
category1.url = "/shop/catalog/accessories"
category1.queryURL = "accessories"
category1.save()

category4 = pmod.Category()
category4.name = "Rental"
category4.is_active = True
category4.imagePath = "base_app/images/nikon200mm.jpg"
category4.url = "/shop/catalog/rentals"
category4.queryURL = "rentals"
category4.save()

stocked = pmod.InventoryType()
stocked.name = "Stocked"
stocked.save()

serialized = pmod.InventoryType()
serialized.name = "Serialized"
serialized.save()

g = pmod.CatalogProduct()
g.inventorytype = stocked
g.catalogID = "A7774747"
g.name = "AA Batteries"
g.description = "Batteries"
g.brand = "Energizer"
g.lname = g.name.lower()
g.ldescription = g.description.lower()
g.lbrand = g.brand.lower()
g.imagePath = "base_app/images/battery.jpg"
g.category = category1
g.price = 2.99
g.rentalPrice = 0
g.replacementPrice = 0
g.is_active = True
g.save()

stockedBats = pmod.StockedProduct()
stockedBats.catalogID = g
stockedBats.amount = 100
stockedBats.amountAvailable = 100
stockedBats.cost = 1.49
stockedBats.store = a
stockedBats.is_active = True
stockedBats.save()

stockedBats1 = pmod.StockedProduct()
stockedBats1.catalogID = g
stockedBats1.amount = 100
stockedBats1.amountAvailable = 100
stockedBats1.cost = 1.89
stockedBats1.store = b
stockedBats1.is_active = True
stockedBats1.save()

stockedBats2 = pmod.StockedProduct()
stockedBats2.catalogID = g
stockedBats2.amount = 100
stockedBats2.amountAvailable = 100
stockedBats2.cost = 1.19
stockedBats2.store = c
stockedBats2.is_active = True
stockedBats2.save()

h = pmod.CatalogProduct()
h.inventorytype = serialized
h.catalogID = "B1231232"
h.name = "Power Lens"
h.lname = h.name.lower()
h.description = "High zoom lens"
h.ldescription = h.description.lower()
h.brand = "Sigma"
h.lbrand = h.brand.lower()
h.category = category1
h.price = 149.99
h.imagePath = "base_app/images/sigma10-20mm.jpg"
h.rentalPrice = 10
h.replacementPrice = 250 
h.is_active = True
h.save()

lens0 = pmod.SerializedProduct()
lens0.catalogID = h
lens0.serialNumber = "ABCDEFG0"
lens0.cost = 99.99
lens0.store = a
lens0.is_rental = False
lens0.is_available = True
lens0.is_new = True
lens0.is_active = True
lens0.save()

lens01 = pmod.SerializedProduct()
lens01.catalogID = h
lens01.serialNumber = "ABCDEFG01"
lens01.cost = 99.99
lens01.store = a
lens01.is_rental = False
lens01.is_available = True
lens01.is_new = True
lens01.is_active = True
lens01.save()

lens02 = pmod.SerializedProduct()
lens02.catalogID = h
lens02.serialNumber = "ABCDEFG02"
lens02.cost = 99.99
lens02.store = a
lens02.is_rental = False
lens02.is_available = True
lens02.is_new = True
lens02.is_active = True
lens02.save()

lens03 = pmod.SerializedProduct()
lens03.catalogID = h
lens03.serialNumber = "ABCDEFG03"
lens03.cost = 99.99
lens03.store = a
lens03.is_rental = False
lens03.is_available = True
lens03.is_new = True
lens03.is_active = True
lens03.save()

lens04 = pmod.SerializedProduct()
lens04.catalogID = h
lens04.serialNumber = "ABCDEFG04"
lens04.cost = 99.99
lens04.store = a
lens04.is_rental = False
lens04.is_available = True
lens04.is_new = True
lens04.is_active = True
lens04.save()

lens05 = pmod.SerializedProduct()
lens05.catalogID = h
lens05.serialNumber = "ABCDEFG05"
lens05.cost = 99.99
lens05.store = a
lens05.is_rental = False
lens05.is_available = True
lens05.is_new = True
lens05.is_active = True
lens05.save()

lens06 = pmod.SerializedProduct()
lens06.catalogID = h
lens06.serialNumber = "ABCDEFG06"
lens06.cost = 99.99
lens06.store = a
lens06.is_rental = False
lens06.is_available = True
lens06.is_new = True
lens06.is_active = True
lens06.save()

lens07 = pmod.SerializedProduct()
lens07.catalogID = h
lens07.serialNumber = "ABCDEFG07"
lens07.cost = 99.99
lens07.store = a
lens07.is_rental = False
lens07.is_available = True
lens07.is_new = True
lens07.is_active = True
lens07.save()

lens08 = pmod.SerializedProduct()
lens08.catalogID = h
lens08.serialNumber = "ABCDEFG08"
lens08.cost = 99.99
lens08.store = a
lens08.is_rental = False
lens08.is_available = True
lens08.is_new = True
lens08.is_active = True
lens08.save()

lens09 = pmod.SerializedProduct()
lens09.catalogID = h
lens09.serialNumber = "ABCDEFG09"
lens09.cost = 99.99
lens09.store = a
lens09.is_rental = False
lens09.is_available = True
lens09.is_new = True
lens09.is_active = True
lens09.save()

lens00 = pmod.SerializedProduct()
lens00.catalogID = h
lens00.serialNumber = "ABCDEFG00"
lens00.cost = 99.99
lens00.store = a
lens00.is_rental = False
lens00.is_available = True
lens00.is_new = True
lens00.is_active = True
lens00.save()

i = pmod.CatalogProduct()
i.inventorytype = stocked
i.catalogID = "C23213123"
i.name = "Kit Cleaner"
i.description = "Cleaner for lenses"
i.brand = "Nikon"
i.lname = i.name.lower()
i.ldescription = i.description.lower()
i.lbrand = i.brand.lower()
i.category = category1
i.imagePath = "base_app/images/kitnikon.jpg"
i.price = 19.99
i.rentalPrice = 0
i.replacementPrice = 0
i.is_active = True
i.save()

i2 = pmod.CatalogProduct()
i2.inventorytype = stocked
i2.catalogID = "C45513123"
i2.name = "Handheld base"
i2.description = "Handheld unipod for cameras"
i2.brand = "Opteka"
i2.lname = i2.name.lower()
i2.ldescription = i2.description.lower()
i2.lbrand = i2.brand.lower()
i2.category = category1
i2.imagePath = "base_app/images/handpod.jpg"
i2.price = 30.99
i2.rentalPrice = 10
i2.replacementPrice = 0
i2.is_active = True
i2.save()


i99 = pmod.CatalogProduct()
i99.inventorytype = stocked
i99.catalogID = "B875513123"
i99.name = "Flash DSLR"
i99.description = "High Potency Flash"
i99.brand = "Yundour"
i99.lname = i99.name.lower()
i99.ldescription = i99.description.lower()
i99.lbrand = i99.brand.lower()
i99.category = category1
i99.imagePath = "base_app/images/flash.jpg"
i99.price = 99.99
i99.rentalPrice = 25
i99.replacementPrice = 45
i99.is_active = True
i99.save()

stockedClean99 = pmod.StockedProduct()
stockedClean99.catalogID = i99
stockedClean99.amount = 100
stockedClean99.amountAvailable = 100
stockedClean99.cost = 110.00
stockedClean99.store = a
stockedClean99.is_active = True
stockedClean99.save()

stockedClean = pmod.StockedProduct()
stockedClean.catalogID = i
stockedClean.amount = 100
stockedClean.amountAvailable = 100
stockedClean.cost = 11.00
stockedClean.store = a
stockedClean.is_active = True
stockedClean.save()

stockedClean11 = pmod.StockedProduct()
stockedClean11.catalogID = i2
stockedClean11.amount = 100
stockedClean11.amountAvailable = 100
stockedClean11.cost = 30.00
stockedClean11.store = a
stockedClean11.is_active = True
stockedClean11.save()

stockedClean1 = pmod.StockedProduct()
stockedClean1.catalogID = i
stockedClean1.amount = 100
stockedClean1.amountAvailable = 100
stockedClean1.cost = 8.89
stockedClean1.store = b
stockedClean1.is_active = True
stockedClean1.save()

stockedClean2 = pmod.StockedProduct()
stockedClean2.catalogID = i
stockedClean2.amount = 100
stockedClean2.amountAvailable = 100
stockedClean2.cost = 9.99
stockedClean2.store = c
stockedClean2.is_active = True
stockedClean2.save()

j = pmod.CatalogProduct()
j.inventorytype = serialized
j.catalogID = "V2123456987"
j.name = "Vivitar Video Camera"
j.description = "Video camera"
j.brand = "Vivitar"
j.imagePath = "base_app/images/vivitar.jpg"
j.lname = j.name.lower()
j.ldescription = j.description.lower()
j.lbrand = j.brand.lower()
j.category = category2
j.price = 699.99
j.rentalPrice = 55
j.replacementPrice = 877 
j.is_active = True
j.save()

v1 = pmod.CatalogProduct()
v1.inventorytype = serialized
v1.catalogID = "V1123456987"
v1.name = "Contour Video Camera"
v1.description = "Video camera"
v1.brand = "Contour"
v1.imagePath = "base_app/images/videocam.jpg"
v1.lname = v1.name.lower()
v1.ldescription = v1.description.lower()
v1.lbrand = v1.brand.lower()
v1.category = category2
v1.price = 450.99
v1.rentalPrice = 40
v1.replacementPrice = 998 
v1.is_active = True
v1.save()

v2 = pmod.CatalogProduct()
v2.inventorytype = serialized
v2.catalogID = "V3123456987"
v2.name = "Sony Video Camera"
v2.description = "Video camera"
v2.brand = "Sony"
v2.imagePath = "base_app/images/sonyvideo.jpg"
v2.lname = v2.name.lower()
v2.ldescription = v2.description.lower()
v2.lbrand = v2.brand.lower()
v2.category = category2
v2.price = 350.99
v2.rentalPrice = 50
v2.replacementPrice = 450 
v2.is_active = True
v2.save()

dc70 = pmod.SerializedProduct()
dc70.catalogID = j
dc70.serialNumber = "DCABCDEFG0"
dc70.cost = 299.99
dc70.store = a
dc70.is_rental = True
dc70.is_available = True
dc70.is_new = True
dc70.is_active = True
dc70.save()

dc701 = pmod.SerializedProduct()
dc701.catalogID = j
dc701.serialNumber = "DCABCDEFG01"
dc701.cost = 299.99
dc701.store = a
dc701.is_rental = True
dc701.is_available = True
dc701.is_new = True
dc701.is_active = True
dc701.save()

dc702 = pmod.SerializedProduct()
dc702.catalogID = j
dc702.serialNumber = "DCABCDEFG02"
dc702.cost = 299.99
dc702.store = a
dc702.is_rental = False
dc702.is_available = True
dc702.is_new = True
dc702.is_active = True
dc702.save()

dc703 = pmod.SerializedProduct()
dc703.catalogID = j
dc703.serialNumber = "DCABCDEFG03"
dc703.cost = 299.99
dc703.store = a
dc703.is_rental = False
dc703.is_available = True
dc703.is_new = True
dc703.is_active = True
dc703.save()

dc704 = pmod.SerializedProduct()
dc704.catalogID = j
dc704.serialNumber = "DCABCDEFG04"
dc704.cost = 299.99
dc704.store = a
dc704.is_rental = False
dc704.is_available = True
dc704.is_new = True
dc704.is_active = True
dc704.save()

dc705 = pmod.SerializedProduct()
dc705.catalogID = j
dc705.serialNumber = "DCABCDEFG05"
dc705.cost = 299.99
dc705.store = a
dc705.is_rental = True
dc705.is_available = True
dc705.is_new = True
dc705.is_active = True
dc705.save()

dc706 = pmod.SerializedProduct()
dc706.catalogID = j
dc706.serialNumber = "DCABCDEFG06"
dc706.cost = 299.99
dc706.store = a
dc706.is_rental = True
dc706.is_available = True
dc706.is_new = True
dc706.is_active = True
dc706.save()

dc707 = pmod.SerializedProduct()
dc707.catalogID = j
dc707.serialNumber = "DCABCDEFG07"
dc707.cost = 299.99
dc707.store = a
dc707.is_rental = False
dc707.is_available = True
dc707.is_new = True
dc707.is_active = True
dc707.save()

dc708 = pmod.SerializedProduct()
dc708.catalogID = j
dc708.serialNumber = "DCABCDEFG08"
dc708.cost = 299.99
dc708.store = a
dc708.is_rental = False
dc708.is_available = True
dc708.is_new = True
dc708.is_active = True
dc708.save()

dc709 = pmod.SerializedProduct()
dc709.catalogID = j
dc709.serialNumber = "DCABCDEFG09"
dc709.cost = 299.99
dc709.store = a
dc709.is_rental = False
dc709.is_available = True
dc709.is_new = True
dc709.is_active = True
dc709.save()

dc700 = pmod.SerializedProduct()
dc700.catalogID = j
dc700.serialNumber = "DCABCDEFG00"
dc700.cost = 299.99
dc700.store = a
dc700.is_rental = True
dc700.is_available = True
dc700.is_new = True
dc700.is_active = True
dc700.save()

ja = pmod.CatalogProduct()
ja.inventorytype = serialized
ja.catalogID = "NK9089"
ja.name = "Nikon D3100"
ja.description = "Camera made especially for fireworks!"
ja.brand = "Nikon"
ja.imagePath = "base_app/images/nikond3100.jpg"
ja.lname = ja.name.lower()
ja.ldescription = ja.description.lower()
ja.lbrand = ja.brand.lower()
ja.category = category3
ja.price = 899.99
ja.rentalPrice = 20.99
ja.replacementPrice = 650.99
ja.is_active = True
ja.save()

niko550 = pmod.SerializedProduct()
niko550.catalogID = ja
niko550.serialNumber = "NIKODCABCDEFG0"
niko550.cost = 99.99
niko550.store = a
niko550.is_rental = True
niko550.is_available = True
niko550.is_new = True
niko550.is_active = True
niko550.save()

niko5501 = pmod.SerializedProduct()
niko5501.catalogID = ja
niko5501.serialNumber = "NIKODCABCDEFG01"
niko5501.cost = 99.99
niko5501.store = a
niko5501.is_rental = False
niko5501.is_available = True
niko5501.is_new = True
niko5501.is_active = True
niko5501.save()

niko5502 = pmod.SerializedProduct()
niko5502.catalogID = ja
niko5502.serialNumber = "NIKODCABCDEFG02"
niko5502.cost = 99.99
niko5502.store = a
niko5502.is_rental = True
niko5502.is_available = True
niko5502.is_new = True
niko5502.is_active = True
niko5502.save()

niko5503 = pmod.SerializedProduct()
niko5503.catalogID = ja
niko5503.serialNumber = "NIKODCABCDEFG03"
niko5503.cost = 99.99
niko5503.store = a
niko5503.is_rental = False
niko5503.is_available = True
niko5503.is_new = True
niko5503.is_active = True
niko5503.save()

niko5504 = pmod.SerializedProduct()
niko5504.catalogID = ja
niko5504.serialNumber = "NIKODCABCDEFG04"
niko5504.cost = 99.99
niko5504.store = a
niko5504.is_rental = True
niko5504.is_available = True
niko5504.is_new = True
niko5504.is_active = True
niko5504.save()

niko5505 = pmod.SerializedProduct()
niko5505.catalogID = ja
niko5505.serialNumber = "NIKODCABCDEFG05"
niko5505.cost = 99.99
niko5505.store = b
niko5505.is_rental = False
niko5505.is_available = True
niko5505.is_new = True
niko5505.is_active = True
niko5505.save()

niko5506 = pmod.SerializedProduct()
niko5506.catalogID = ja
niko5506.serialNumber = "NIKODCABCDEFG06"
niko5506.cost = 99.99
niko5506.store = b
niko5506.is_rental = False
niko5506.is_available = True
niko5506.is_new = True
niko5506.is_active = True
niko5506.save()

niko5507 = pmod.SerializedProduct()
niko5507.catalogID = ja
niko5507.serialNumber = "NIKODCABCDEFG07"
niko5507.cost = 99.99
niko5507.store = c
niko5507.is_rental = True
niko5507.is_available = True
niko5507.is_new = True
niko5507.is_active = True
niko5507.save()

niko5508 = pmod.SerializedProduct()
niko5508.catalogID = ja
niko5508.serialNumber = "NIKODCABCDEFG08"
niko5508.cost = 99.99
niko5508.store = a
niko5508.is_rental = False
niko5508.is_available = True
niko5508.is_new = True
niko5508.is_active = True
niko5508.save()

niko5509 = pmod.SerializedProduct()
niko5509.catalogID = ja
niko5509.serialNumber = "NIKODCABCDEFG09"
niko5509.cost = 99.99
niko5509.store = b
niko5509.is_rental = False
niko5509.is_available = True
niko5509.is_new = True
niko5509.is_active = True
niko5509.save()

niko5500 = pmod.SerializedProduct()
niko5500.catalogID = ja
niko5500.serialNumber = "NIKODCABCDEFG00"
niko5500.cost = 99.99
niko5500.store = c
niko5500.is_rental = True
niko5500.is_available = True
niko5500.is_new = True
niko5500.is_active = True
niko5500.save()

jab = pmod.CatalogProduct()
jab.inventorytype = serialized
jab.catalogID = "FF99"
jab.name = "Sony Cam"
jab.description = "Video camera with special YouTube capability"
jab.brand = "Sony"
jab.imagePath = "base_app/images/vsony.jpg"
jab.lname = jab.name.lower()
jab.ldescription = jab.description.lower()
jab.lbrand = jab.brand.lower()
jab.category = category2
jab.price = 299.99
jab.rentalPrice = 19.99
jab.replacementPrice = 199.99 
jab.is_active = True
jab.save()

fuji0 = pmod.SerializedProduct()
fuji0.catalogID = jab
fuji0.serialNumber = "FUJINIKODCABCDEFG0"
fuji0.cost = 99.99
fuji0.store = a
fuji0.is_rental = False
fuji0.is_available = True
fuji0.is_new = True
fuji0.is_active = True
fuji0.save()

fuji01 = pmod.SerializedProduct()
fuji01.catalogID = jab
fuji01.serialNumber = "FUJINIKODCABCDEFG01"
fuji01.cost = 99.99
fuji01.store = a
fuji01.is_rental = False
fuji01.is_available = True
fuji01.is_new = True
fuji01.is_active = True
fuji01.save()

fuji02 = pmod.SerializedProduct()
fuji02.catalogID = jab
fuji02.serialNumber = "FUJINIKODCABCDEFG02"
fuji02.cost = 99.99
fuji02.store = a
fuji02.is_rental = False
fuji02.is_available = True
fuji02.is_new = True
fuji02.is_active = True
fuji02.save()

fuji03 = pmod.SerializedProduct()
fuji03.catalogID = jab
fuji03.serialNumber = "FUJINIKODCABCDEFG03"
fuji03.cost = 99.99
fuji03.store = a
fuji03.is_rental = False
fuji03.is_available = True
fuji03.is_new = True
fuji03.is_active = True
fuji03.save()

fuji04 = pmod.SerializedProduct()
fuji04.catalogID = jab
fuji04.serialNumber = "FUJINIKODCABCDEFG04"
fuji04.cost = 99.99
fuji04.store = a
fuji04.is_rental = False
fuji04.is_available = True
fuji04.is_new = True
fuji04.is_active = True
fuji04.save()

fuji05 = pmod.SerializedProduct()
fuji05.catalogID = jab
fuji05.serialNumber = "FUJINIKODCABCDEFG05"
fuji05.cost = 99.99
fuji05.store = b
fuji05.is_rental = False
fuji05.is_available = True
fuji05.is_new = True
fuji05.is_active = True
fuji05.save()

fuji06 = pmod.SerializedProduct()
fuji06.catalogID = jab
fuji06.serialNumber = "FUJINIKODCABCDEFG06"
fuji06.cost = 99.99
fuji06.store = b
fuji06.is_rental = True
fuji06.is_available = True
fuji06.is_new = True
fuji06.is_active = True
fuji06.save()

fuji07 = pmod.SerializedProduct()
fuji07.catalogID = jab
fuji07.serialNumber = "FUJINIKODCABCDEFG07"
fuji07.cost = 99.99
fuji07.store = c
fuji07.is_rental = False
fuji07.is_available = True
fuji07.is_new = True
fuji07.is_active = True
fuji07.save()

fuji08 = pmod.SerializedProduct()
fuji08.catalogID = jab
fuji08.serialNumber = "FUJINIKODCABCDEFG08"
fuji08.cost = 99.99
fuji08.store = a
fuji08.is_rental = False
fuji08.is_available = True
fuji08.is_new = True
fuji08.is_active = True
fuji08.save()

fuji09 = pmod.SerializedProduct()
fuji09.catalogID = jab
fuji09.serialNumber = "FUJINIKODCABCDEFG09"
fuji09.cost = 99.99
fuji09.store = b
fuji09.is_rental = False
fuji09.is_available = True
fuji09.is_new = True
fuji09.is_active = True
fuji09.save()

fuji00 = pmod.SerializedProduct()
fuji00.catalogID = jab
fuji00.serialNumber = "FUJINIKODCABCDEFG00"
fuji00.cost = 99.99
fuji00.store = c
fuji00.is_rental = False
fuji00.is_available = True
fuji00.is_new = True
fuji00.is_active = True
fuji00.save()


jabb = pmod.CatalogProduct()
jabb.inventorytype = serialized
jabb.catalogID = "S909"
jabb.name = "Nikon 520"
jabb.description = "High speed camera with two lenses"
jabb.brand = "Nikon"
jabb.imagePath = "base_app/images/nikonp520.jpg"
jabb.lname = jabb.name.lower()
jabb.ldescription = jabb.description.lower()
jabb.lbrand = jabb.brand.lower()
jabb.category = category3
jabb.price = 999.99
jabb.rentalPrice = 69.99
jabb.replacementPrice = 799.99
jabb.is_active = True
jabb.save()

sony4540 = pmod.SerializedProduct()
sony4540.catalogID = jabb
sony4540.serialNumber = "SONY898EFG0"
sony4540.cost = 499.99
sony4540.store = a
sony4540.is_rental = False
sony4540.is_available = True
sony4540.is_new = True
sony4540.is_active = True
sony4540.save()

sony45401 = pmod.SerializedProduct()
sony45401.catalogID = jabb
sony45401.serialNumber = "SONY898EFG01"
sony45401.cost = 499.99
sony45401.store = a
sony45401.is_rental = False
sony45401.is_available = True
sony45401.is_new = True
sony45401.is_active = True
sony45401.save()

sony45402 = pmod.SerializedProduct()
sony45402.catalogID = jabb
sony45402.serialNumber = "SONY898EFG02"
sony45402.cost = 499.99
sony45402.store = a
sony45402.is_rental = True
sony45402.is_available = True
sony45402.is_new = True
sony45402.is_active = True
sony45402.save()

sony45403 = pmod.SerializedProduct()
sony45403.catalogID = jabb
sony45403.serialNumber = "SONY898EFG03"
sony45403.cost = 499.99
sony45403.store = a
sony45403.is_rental = False
sony45403.is_available = True
sony45403.is_new = True
sony45403.is_active = True
sony45403.save()

sony45404 = pmod.SerializedProduct()
sony45404.catalogID = jabb
sony45404.serialNumber = "SONY898EFG04"
sony45404.cost = 499.99
sony45404.store = a
sony45404.is_rental = True
sony45404.is_available = True
sony45404.is_new = True
sony45404.is_active = True
sony45404.save()

sony45405 = pmod.SerializedProduct()
sony45405.catalogID = jabb
sony45405.serialNumber = "SONY898EFG05"
sony45405.cost = 499.99
sony45405.store = b
sony45405.is_rental = False
sony45405.is_available = True
sony45405.is_new = True
sony45405.is_active = True
sony45405.save()

sony45406 = pmod.SerializedProduct()
sony45406.catalogID = jabb
sony45406.serialNumber = "SONY898EFG06"
sony45406.cost = 499.99
sony45406.store = b
sony45406.is_rental = False
sony45406.is_available = True
sony45406.is_new = True
sony45406.is_active = True
sony45406.save()

sony45407 = pmod.SerializedProduct()
sony45407.catalogID = jabb
sony45407.serialNumber = "SONY898EFG07"
sony45407.cost = 499.99
sony45407.store = c
sony45407.is_rental = False
sony45407.is_available = True
sony45407.is_new = True
sony45407.is_active = True
sony45407.save()

sony45408 = pmod.SerializedProduct()
sony45408.catalogID = jabb
sony45408.serialNumber = "SONY898EFG08"
sony45408.cost = 499.99
sony45408.store = a
sony45408.is_rental = True
sony45408.is_available = True
sony45408.is_new = True
sony45408.is_active = True
sony45408.save()

sony45409 = pmod.SerializedProduct()
sony45409.catalogID = jabb
sony45409.serialNumber = "SONY898EFG09"
sony45409.cost = 499.99
sony45409.store = b
sony45409.is_rental = False
sony45409.is_available = True
sony45409.is_new = True
sony45409.is_active = True
sony45409.save()

sony45400 = pmod.SerializedProduct()
sony45400.catalogID = jabb
sony45400.serialNumber = "SONY898EFG00"
sony45400.cost = 499.99
sony45400.store = c
sony45400.is_rental = False
sony45400.is_available = True
sony45400.is_new = True
sony45400.is_active = True
sony45400.save()


jabba = pmod.CatalogProduct()
jabba.inventorytype = stocked
jabba.catalogID = "K4565"
jabba.name = "Kingston 32GB SD"
jabba.description = "32GB SD card for holding your photos/videos."
jabba.brand = "Kingston"
jabba.imagePath = "base_app/images/sd1.jpg"
jabba.lname = jabba.name.lower()
jabba.ldescription = jabba.description.lower()
jabba.lbrand = jabba.brand.lower()
jabba.category = category1
jabba.price = 19.99
jabba.rentalPrice = 0
jabba.replacementPrice = 0
jabba.is_active = True
jabba.save()

stockedCard = pmod.StockedProduct()
stockedCard.catalogID = jabba
stockedCard.amount = 100
stockedCard.amountAvailable = 100
stockedCard.cost = 7.45
stockedCard.store = a
stockedCard.is_active = True
stockedCard.save()

stockedCard1 = pmod.StockedProduct()
stockedCard1.catalogID = jabba
stockedCard1.amount = 100
stockedCard1.amountAvailable = 100
stockedCard1.cost = 6.33
stockedCard1.store = b
stockedCard1.is_active = True
stockedCard1.save()

stockedCard2 = pmod.StockedProduct()
stockedCard2.catalogID = jabba
stockedCard2.amount = 100
stockedCard2.amountAvailable = 100
stockedCard2.cost = 9.87
stockedCard2.store = c
stockedCard2.is_active = True
stockedCard2.save()

visa = pmod.CardType()
visa.name = "Visa"
visa.save()

mc = pmod.CardType()
mc.name = "Master Card"
mc.save()

ae = pmod.CardType()
ae.name = "American Express"
ae.save()

online = pmod.TransactionType()
online.transactiontype = "OnlineSale"
online.save()

rental = pmod.TransactionType()
rental.transactiontype = "Rental"
rental.save()

repair = pmod.TransactionType()
repair.transactiontype = "Repair"
repair.save()

inprogress = pmod.RepairStatus()
inprogress.status = "In Progress"
inprogress.save()

completed = pmod.RepairStatus()
completed.status = "Completed"
completed.save()

so1 = pmod.ShippingOption()
so1.daystoarrive = 1
so1.price = 14.99
so1.save()

so2 = pmod.ShippingOption()
so2.daystoarrive = 3
so2.price = 8.99
so2.save()

so3 = pmod.ShippingOption()
so3.daystoarrive = 5
so3.price = 0
so3.save()


default = pmod.TaxRates()
default.state = "default"
default.taxRate = 0.06
default.save()

sub1 = pmod.Subledger()
sub1.type = "Inventory"
sub1.save()

sub2 = pmod.Subledger()
sub2.type = "Cost of Goods Sold"
sub2.save()


sub3 = pmod.Subledger()
sub3.type = "Sales"
sub3.save()

sub4 = pmod.Subledger()
sub4.type = "Cash"
sub4.save()
