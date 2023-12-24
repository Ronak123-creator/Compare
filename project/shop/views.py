from django.shortcuts import render, get_object_or_404,get_list_or_404
from .models import *
from .scrap2 import scrape_and_insert
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from .infotech import scrapinfo
from .itti_dell import scrape_and_insert1
import re
from django.db import transaction
import pandas as pd
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from operator import itemgetter
from .neop import scrapNeoPhone
from .dealayo import scrapPhone

def home(request):
    products_list = Filtered.objects.exclude(brand="Apple").exclude(brand="MacBook")
    best = best_laptop_score(products_list)
    gaming = best_laptop_gaming(products_list)
    best_under = best_laptop_120000_150000(products_list)
    best_under_120000 = best_laptop_90000_120000(products_list)
    best_under_90000 = best_laptop_60000_90000(products_list)
    best_under_60000 = best_laptop_below_60000(products_list)
    context = {
               'gaming':gaming,
               'best':best,
               'best_under':best_under,
               'best_under_120000':best_under_120000,
               'best_under_90000':best_under_90000,
               'best_under_60000':best_under_60000}
    return render(request, 'home.html', context)


def best_laptop_gaming(products):
    max_cpu_rank = 243
    max_gpu_rank = 75
    max_ram_rank = 11
    max_storage_rank = 2
    max_memory = 5
    
    weights = {'cpu': 0.5, 'gpu': 0.5, 'ram': 0.3, 'storage': 0.3, 'memory': 0.3}

    # Create a list to store gaming products
    gaming_products = []

    for product in products:
        # Check if the processor_info contains the "H" suffix (case insensitive)
        if 'H' in product.processor_info.upper():
            # Check if "NVIDIA" or "RTX" is present in graphics_info (case insensitive)
            if 'NVIDIA' in product.graphics_info.upper() or 'RTX' in product.graphics_info.upper():
                normalized_cpu_score = rankProcessor(product.processor_info) / max_cpu_rank
                normalized_gpu_score = rankGpu(product.graphics_info) / max_gpu_rank
                normalized_ram_score = rankRam(product.ram) / max_ram_rank
                normalized_storage_score = rankStorage(product.storage_type) / max_storage_rank
                normalized_memory_score = rankStorage_info(product.storage) / max_memory

                score = (weights['cpu'] * normalized_cpu_score + 
                         weights['gpu'] * normalized_gpu_score +
                         weights['ram'] * normalized_ram_score +
                         weights['storage'] * normalized_storage_score +
                         weights['memory'] * normalized_memory_score )

                setattr(product, 'score', score)

                # Add the product to the gaming_products list
                gaming_products.append(product)

    # Sort the gaming_products based on their scores
    sorted_products = sorted(gaming_products, key=lambda x: getattr(x, 'score', 0), reverse=True)[:12]
    return sorted_products





def best_laptop_score(products):
    max_cpu_rank = 243
    max_gpu_rank = 75
    max_ram_rank = 11
    max_storage_rank = 2
    max_memory = 5
    
    weights = {'cpu': 0.5, 'gpu': 0.5, 'ram': 0.3, 'storage': 0.3, 'memory':0.3}

    for product in products:
        normalized_cpu_score = rankProcessor(product.processor_info) / max_cpu_rank
        normalized_gpu_score = rankGpu(product.graphics_info) / max_gpu_rank
        normalized_ram_score = rankRam(product.ram) / max_ram_rank
        normalized_storage_score = rankStorage(product.storage_type) / max_storage_rank
        normalized_memory_score = rankStorage_info(product.storage) / max_memory

        score = (weights['cpu'] * normalized_cpu_score + 
                 weights['gpu'] * normalized_gpu_score +
                 weights['ram'] * normalized_ram_score +
                 weights['storage'] * normalized_storage_score +
                 weights['memory'] * normalized_memory_score )
        
        setattr(product, 'score', score)

    sorted_products = sorted(products, key=lambda x: getattr(x, 'score', 0), reverse=True)[:12]  
    return sorted_products

def best_laptop_120000_150000(products):
    max_cpu_rank = 243
    max_gpu_rank = 75
    max_ram_rank = 11
    max_storage_rank = 2
    max_memory = 5
    
    weights = {'cpu': 0.5, 'gpu': 0.5, 'ram': 0.3, 'storage': 0.3, 'memory':0.3}

    filtered_products = [product for product in products if 120000 <= int(float(product.price)) <= 150000]


    for product in filtered_products:
        normalized_cpu_score = rankProcessor(product.processor_info) / max_cpu_rank
        normalized_gpu_score = rankGpu(product.graphics_info) / max_gpu_rank
        normalized_ram_score = rankRam(product.ram) / max_ram_rank
        normalized_storage_score = rankStorage(product.storage_type) / max_storage_rank
        normalized_memory_score = rankStorage_info(product.storage) / max_memory

        score = (weights['cpu'] * normalized_cpu_score + 
                 weights['gpu'] * normalized_gpu_score +
                 weights['ram'] * normalized_ram_score +
                 weights['storage'] * normalized_storage_score +
                 weights['memory'] * normalized_memory_score)
        
        setattr(product, 'score', score)

    sorted_products = sorted(filtered_products, key=lambda x: getattr(x, 'score', 0), reverse=True)[:12]
    return sorted_products

def best_laptop_90000_120000(products):
    max_cpu_rank = 243
    max_gpu_rank = 75
    max_ram_rank = 11
    max_storage_rank = 2
    max_memory = 5
    
    weights = {'cpu': 0.5, 'gpu': 0.5, 'ram': 0.1, 'storage': 0.1, 'memory':0.2}

    filtered_products = [product for product in products if 90000 <= int(float(product.price)) <= 120000]


    for product in filtered_products:
        normalized_cpu_score = rankProcessor(product.processor_info) / max_cpu_rank
        normalized_gpu_score = rankGpu(product.graphics_info) / max_gpu_rank
        normalized_ram_score = rankRam(product.ram) / max_ram_rank
        normalized_storage_score = rankStorage(product.storage_type) / max_storage_rank
        normalized_memory_score = rankStorage_info(product.storage) / max_memory

        score = (weights['cpu'] * normalized_cpu_score + 
                 weights['gpu'] * normalized_gpu_score +
                 weights['ram'] * normalized_ram_score +
                 weights['storage'] * normalized_storage_score +
                 weights['memory'] * normalized_memory_score)
        
        setattr(product, 'score', score)

    sorted_products = sorted(filtered_products, key=lambda x: getattr(x, 'score', 0), reverse=True)[:12]
    return sorted_products

def best_laptop_60000_90000(products):
    max_cpu_rank = 243
    max_gpu_rank = 75
    max_ram_rank = 11
    max_storage_rank = 2
    max_memory = 5
    
    weights = {'cpu': 0.5, 'gpu': 0.5, 'ram': 0.3, 'storage': 0.3, 'memory':0.3}

    filtered_products = [product for product in products if 60000 <= int(float(product.price)) <= 90000]


    for product in filtered_products:
        normalized_cpu_score = rankProcessor(product.processor_info) / max_cpu_rank
        normalized_gpu_score = rankGpu(product.graphics_info) / max_gpu_rank
        normalized_ram_score = rankRam(product.ram) / max_ram_rank
        normalized_storage_score = rankStorage(product.storage_type) / max_storage_rank
        normalized_memory_score = rankStorage_info(product.storage) / max_memory

        score = (weights['cpu'] * normalized_cpu_score + 
                 weights['gpu'] * normalized_gpu_score +
                 weights['ram'] * normalized_ram_score +
                 weights['storage'] * normalized_storage_score +
                 weights['memory'] * normalized_memory_score)
        
        setattr(product, 'score', score)

    sorted_products = sorted(filtered_products, key=lambda x: getattr(x, 'score', 0), reverse=True)[:12]
    return sorted_products

def best_laptop_below_60000(products):
    max_cpu_rank = 243
    max_gpu_rank = 75
    max_ram_rank = 11
    max_storage_rank = 2
    max_memory = 5
    
    weights = {'cpu': 0.5, 'gpu': 0.5, 'ram': 0.3, 'storage': 0.3, 'memory':0.3}

    filtered_products = [product for product in products if 10000 <= int(float(product.price)) <= 60000]


    for product in filtered_products:
        normalized_cpu_score = rankProcessor(product.processor_info) / max_cpu_rank
        normalized_gpu_score = rankGpu(product.graphics_info) / max_gpu_rank
        normalized_ram_score = rankRam(product.ram) / max_ram_rank
        normalized_storage_score = rankStorage(product.storage_type) / max_storage_rank
        normalized_memory_score = rankStorage_info(product.storage) / max_memory

        score = (weights['cpu'] * normalized_cpu_score + 
                 weights['gpu'] * normalized_gpu_score +
                 weights['ram'] * normalized_ram_score +
                 weights['storage'] * normalized_storage_score +
                 weights['memory'] * normalized_memory_score)
        
        setattr(product, 'score', score)

    sorted_products = sorted(filtered_products, key=lambda x: getattr(x, 'score', 0), reverse=True)[:12]
    return sorted_products

def laptop(request):
    products_list = Filtered.objects.exclude(brand="Apple").exclude(brand="MacBook")
    paginator = Paginator(products_list, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products':products}
    return render (request, 'laptop.html', context)

def Smartphone(request):
    return render (request, 'smartphone.html')



def search_results(request):
    query = request.GET.get('q')
    print(f"Query: {query}")  # Debugging line

    if query:
        search_list = Filtered.objects.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query)
        )
        paginator = Paginator(search_list, 12)
        page = request.GET.get('page')
        search_results = paginator.get_page(page)
    else:
        search_results = Filtered.objects.none()

    return render(request, 'search_results.html', {'search_results': search_results})

def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')

# def mapProducts():
#     result1 = scrape_and_insert()
#     return HttpResponse(result1) 

def scrap_products(request):
    try:
        scrape_and_insert()
        scrape_and_insert1()
        scrapinfo()
        scrapPhone()
        scrapNeoPhone()
        filterr(request)
        messages.success(request, "Product data were successfully extracted.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    
    return HttpResponseRedirect("/admin")


def detail(request, product_id):
    product = get_object_or_404(Filtered, id=product_id)
    similar_products = find_similar_products(product)
    similar_price = find_similar_price(product)
    context = {
        "product": product,
        "similar_products":similar_products,
        "similar_price":similar_price,
    }
    return render(request, 'detail.html', context)



def find_similar_price(product):
    similar_products = []

    print("Finding similar products for:", product)

    # Find similar products in FilteredNeo model
    neo_similar_products = FilteredNeo.objects.filter(brand=product.brand, model=product.model, ram=product.ram, processor_info=product.processor_info)
    print("Neo similar products:", neo_similar_products)
    similar_products.extend(neo_similar_products)

    # Find similar products in FilteredItti model
    itti_similar_products = FilteredItti.objects.filter(brand=product.brand, model=product.model, ram=product.ram, processor_info=product.processor_info)
    print("Itti similar products:", itti_similar_products)
    similar_products.extend(itti_similar_products)

    # Sort the similar products based on some criteria, e.g., price
    similar_products.sort(key=lambda x: x.price)

    print("Final similar products:", similar_products)
    return similar_products




def find_similar_products(product):
    same_ram_products = Filtered.objects.filter(ramm=product.ramm)
    similar_products = []

    current_processor_rank = rankProcessor(product.processor_info)
    current_graphics_rank = rankGpu(product.graphics_info)
    current_price = int(float(product.price))
    


    processor_lower_bound = current_processor_rank - 20
    processor_upper_bound = current_processor_rank + 20

    graphics_lower_bound = current_graphics_rank - 10
    graphics_upper_bound = current_graphics_rank + 10

    price_lower_bound = current_price - 25000
    price_upper_bound = current_price + 25000


    for p in same_ram_products:
        if p.id == product.id:
            continue  # Skip the current product

        processor_rank = rankProcessor(p.processor)
        graphics_rank = rankGpu(p.graphics)
        price = int(float(p.price))
        processor_rank = rankProcessor(p.processor_info)
        graphics_rank = rankGpu(p.graphics_info)
        price = int(float(p.price))

        if (processor_lower_bound <= processor_rank <= processor_upper_bound) and \
           (graphics_lower_bound <= graphics_rank <= graphics_upper_bound) and \
           (price_lower_bound <= price <= price_upper_bound):
            similar_products.append(p)

    return similar_products


def compare(request):
    product1_id = request.GET.get('product1')
    product2_id = request.GET.get('product2')
    try:
        product1 = Filtered.objects.filter(id=product1_id)[0]
        ram_rank1 = rankRam(product1.ram)
        processor_rank1 = rankProcessor(product1.processor_info)
        gpu_rank1 = rankGpu(product1.graphics_info)
        storage_rank1 = rankStorage(product1.storage_type)
    except:
        product1 = ""
    try:
        product2 = Filtered.objects.filter(id=product2_id)[0]
        ram_rank2 = rankRam(product2.ram)
        processor_rank2 = rankProcessor(product2.processor_info)
        gpu_rank2 = rankGpu(product2.graphics_info)
        storage_rank2 = rankStorage(product2.storage_type)
    except:
        product2 = ""

    ram1 = compareRam1(ram_rank1,ram_rank2)
    ram2 = compareRam2(ram_rank1,ram_rank2)
    ram3 = compareRam3(ram_rank1,ram_rank2)
    processor1 = compareProcessor1(processor_rank1, processor_rank2)
    processor2 = compareProcessor2(processor_rank1, processor_rank2)
    processor3 = compareProcessor3(processor_rank1, processor_rank2)
    gpu1 = compareGpu1(gpu_rank1,gpu_rank2)
    gpu2 = compareGpu2(gpu_rank1,gpu_rank2)
    gpu3 = compareGpu3(gpu_rank1,gpu_rank2)
    storage1 = compareStorage1(storage_rank1, storage_rank2)
    storage2 = compareStorage2(storage_rank1, storage_rank2)
    storage3 = compareStorage3(storage_rank1, storage_rank2)

    

    context = {
        "ram1":ram1,
        "ram2":ram2,
        "ram3":ram3,
        "processor1":processor1,
        "processor2":processor2,
        "processor3":processor3,
        "product1": product1,
        "product2": product2,
        "gpu1":gpu1,
        "gpu2":gpu2,
        "gpu3":gpu3,
        'storage1':storage1,
        'storage2':storage2,
        'storage3':storage3,
    }
    return render(request, 'compare.html', context)


# def compare(request):
#     product1_id = request.GET.get('product1')
#     product2_id = request.GET.get('product2')
#     product3_id = request.GET.get('product3')
    
#     try:
#         product1 = Filtered.objects.filter(id=product1_id)[0]
#         ram_rank1 = rankRam(product1.ram)
#         processor_rank1 = rankProcessor(product1.processor_info)
#         gpu_rank1 = rankGpu(product1.graphics_info)
#         storage_rank1 = rankStorage(product1.storage_type)
#     except:
#         product1 = ""
    
#     try:
#         product2 = Filtered.objects.filter(id=product2_id)[0]
#         ram_rank2 = rankRam(product2.ram)
#         processor_rank2 = rankProcessor(product2.processor_info)
#         gpu_rank2 = rankGpu(product2.graphics_info)
#         storage_rank2 = rankStorage(product2.storage_type)
#     except:
#         product2 = ""
    
#     try:
#         product3 = Filtered.objects.filter(id=product3_id)[0]
#         ram_rank3 = rankRam(product3.ram)
#         processor_rank3 = rankProcessor(product3.processor_info)
#         gpu_rank3 = rankGpu(product3.graphics_info)
#         storage_rank3 = rankStorage(product3.storage_type)
#     except:
#         product3 = ""

#     ram1 = compareRam1(ram_rank1, ram_rank2, ram_rank3)
#     ram2 = compareRam2(ram_rank1, ram_rank2, ram_rank3)
#     ram3 = compareRam3(ram_rank1, ram_rank2, ram_rank3)
#     processor1 = compareProcessor1(processor_rank1, processor_rank2, processor_rank3)
#     processor2 = compareProcessor2(processor_rank1, processor_rank2, processor_rank3)
#     processor3 = compareProcessor3(processor_rank1, processor_rank2, processor_rank3)
#     gpu1 = compareGpu1(gpu_rank1, gpu_rank2, gpu_rank3)
#     gpu2 = compareGpu2(gpu_rank1, gpu_rank2, gpu_rank3)
#     gpu3 = compareGpu3(gpu_rank1, gpu_rank2, gpu_rank3)
#     storage1 = compareStorage1(storage_rank1, storage_rank2, storage_rank3)
#     storage2 = compareStorage2(storage_rank1, storage_rank2, storage_rank3)
#     storage3 = compareStorage3(storage_rank1, storage_rank2, storage_rank3)
    
#     context = {
#         "ram1": ram1,
#         "ram2": ram2,
#         "ram3": ram3,
#         "processor1": processor1,
#         "processor2": processor2,
#         "processor3": processor3,
#         "product1": product1,
#         "product2": product2,
#         "product3": product3,
#         "gpu1": gpu1,
#         "gpu2": gpu2,
#         "gpu3": gpu3,
#         'storage1': storage1,
#         'storage2': storage2,
#         'storage3': storage3,
#     }

#     return render(request, 'compare.html', context)


def filterr(request):
    products = Product.objects.all()
    processed_products = set()  # To keep track of already processed products
    
    with transaction.atomic():
        for prod in products:
            unique_id = prod.id  # Assuming your Product model has a unique id
            
            # Skip if the product is Apple or has already been processed
            brand = extractBrand(prod.title)
            if brand.lower() == 'apple' or unique_id in processed_products:
                continue
            
            processed_products.add(unique_id)  # Mark the product as processed
            
            try:
                title = prod.title
                brand = extractBrand(prod.title)
                image = prod.image
                link = prod.link
                if brand == "Dell":
                    model = extract_model(prod.title)
                else:
                    model = extract_second_word(prod.title)

                price = extract_price(prod.price)
                pprice = prod.price
                processor = prod.processor
                processor_info = extract_processor_info(prod.title,prod.processor)
                processor_type = extract_processor_type(prod.title)
                generation = extract_generation(prod.title,prod.processor)
                ramm = prod.ram
                ram = extract_ram(prod.title,prod.ram)
                ram_type = extract_ram_type(prod.ram)
                ram_speed = extract_ram_speed(prod.ram)
                graphics = prod.graphics
                graphics_info = extract_graphics_info(prod.graphics)
                graphics_type = extract_graphics_type(prod.graphics)
                sstorage = prod.storage
                storage = extracted_storage(prod.storage)
                display = prod.display
                storage_type = extract_storage_type(prod.storage)
                display_size = extract_display_size(prod.display)
                touchscreen = extract_touchscreen(prod.touchscreen)
                maximum_display_resulation = prod.maximum_display_resulation
                battery = prod.battery
                operating_system = prod.operating_system
                description = prod.description
                color = prod.color
                warrenty = prod.warrenty
                insurance = prod.insurance
                ports_and_connectivity = prod.ports_and_connectivity
                
                # Create and save Filtered instance
                filtered_instance = Filtered(
                title=title,
                brand=brand,
                image=image,
                price = price,
                pprice = pprice,
                link = link,
                model = model,
                processor = processor,
                processor_info = processor_info,
                processor_type = processor_type,
                generation = generation,
                ramm = ramm,
                ram = ram, 
                ram_type = ram_type,
                ram_speed = ram_speed,
                graphics_info = graphics_info,
                graphics = graphics,
                graphics_type = graphics_type,
                sstorage = sstorage,
                storage = storage,
                storage_type = storage_type,
                display = display,
                display_size = display_size,
                touchscreen = touchscreen,
                maximum_display_resulation = maximum_display_resulation,
                battery = battery,
                operating_system = operating_system,
                description = description,
                color = color,
                warrenty = warrenty,
                insurance = insurance,
                ports_and_connectivity = ports_and_connectivity

            )
                
                filtered_instance.full_clean()  # Validate the instance
                filtered_instance.save()
                
            except ValidationError as ve:
                # Handle validation errors
                print(f"Validation Error: {ve}")
                
            except Exception as e:
                # Generic error handling
                print(f"An error occurred: {e}")

    filterrItti(request)
    filterrNeo(request)

def filterrNeo(request):
    products = ProductNeo.objects.all()
    processed_products = set()  # To keep track of already processed products
    
    with transaction.atomic():
        for prod in products:
            unique_id = prod.id  # Assuming your Product model has a unique id
            
            # Skip if the product is Apple or has already been processed
            brand = extractBrand(prod.title)
            if brand.lower() == 'apple' or unique_id in processed_products:
                continue
            
            processed_products.add(unique_id)  # Mark the product as processed
            
            try:
                title = prod.title
                brand = extractBrand(prod.title)
                image = prod.image
                link = prod.link
                if brand == "Dell":
                    model = extract_model(prod.title)
                else:
                    model = extract_second_word(prod.title)

                price = extract_price(prod.price)
                pprice = prod.price
                processor = prod.processor
                processor_info = extract_processor_info(prod.title,prod.processor)
                processor_type = extract_processor_type(prod.title)
                generation = extract_generation(prod.title,prod.processor)
                ramm = prod.ram
                ram = extract_ram(prod.title,prod.ram)
                ram_type = extract_ram_type(prod.ram)
                ram_speed = extract_ram_speed(prod.ram)
                graphics = prod.graphics
                graphics_info = extract_graphics_info(prod.graphics)
                graphics_type = extract_graphics_type(prod.graphics)
                sstorage = prod.storage
                storage = extracted_storage(prod.storage)
                display = prod.display
                storage_type = extract_storage_type(prod.storage)
                display_size = extract_display_size(prod.display)
                touchscreen = extract_touchscreen(prod.touchscreen)
                maximum_display_resulation = prod.maximum_display_resulation
                battery = prod.battery
                operating_system = prod.operating_system
                description = prod.description
                color = prod.color
                warrenty = prod.warrenty
                insurance = prod.insurance
                ports_and_connectivity = prod.ports_and_connectivity
                
                # Create and save Filtered instance
                filtered_instance = FilteredNeo(
                title=title,
                brand=brand,
                image=image,
                price = price,
                pprice = pprice,
                link = link,
                model = model,
                processor = processor,
                processor_info = processor_info,
                processor_type = processor_type,
                generation = generation,
                ramm = ramm,
                ram = ram, 
                ram_type = ram_type,
                ram_speed = ram_speed,
                graphics_info = graphics_info,
                graphics = graphics,
                graphics_type = graphics_type,
                sstorage = sstorage,
                storage = storage,
                storage_type = storage_type,
                display = display,
                display_size = display_size,
                touchscreen = touchscreen,
                maximum_display_resulation = maximum_display_resulation,
                battery = battery,
                operating_system = operating_system,
                description = description,
                color = color,
                warrenty = warrenty,
                insurance = insurance,
                ports_and_connectivity = ports_and_connectivity

            )
                
                filtered_instance.full_clean()  # Validate the instance
                filtered_instance.save()
                
            except ValidationError as ve:
                # Handle validation errors
                print(f"Validation Error: {ve}")
                
            except Exception as e:
                # Generic error handling
                print(f"An error occurred: {e}")

def filterrItti(request):
    products = ProductItti.objects.all()
    processed_products = set()  # To keep track of already processed products
    
    with transaction.atomic():
        for prod in products:
            unique_id = prod.id  # Assuming your Product model has a unique id
            
            # Skip if the product is Apple or has already been processed
            brand = extractBrand(prod.title)
            if brand.lower() == 'apple' or unique_id in processed_products:
                continue
            
            processed_products.add(unique_id)  # Mark the product as processed
            
            try:
                title = prod.title
                brand = extractBrand(prod.title)
                image = prod.image
                link = prod.link
                if brand == "Dell":
                    model = extract_model(prod.title)
                else:
                    model = extract_second_word(prod.title)

                price = extract_price(prod.price)
                pprice = prod.price
                processor = prod.processor
                processor_info = extract_processor_info(prod.title,prod.processor)
                processor_type = extract_processor_type(prod.title)
                generation = extract_generation(prod.title,prod.processor)
                ramm = prod.ram
                ram = extract_ram(prod.title,prod.ram)
                ram_type = extract_ram_type(prod.ram)
                ram_speed = extract_ram_speed(prod.ram)
                graphics = prod.graphics
                graphics_info = extract_graphics_info(prod.graphics)
                graphics_type = extract_graphics_type(prod.graphics)
                sstorage = prod.storage
                storage = extracted_storage(prod.storage)
                display = prod.display
                storage_type = extract_storage_type(prod.storage)
                display_size = extract_display_size(prod.display)
                touchscreen = extract_touchscreen(prod.touchscreen)
                maximum_display_resulation = prod.maximum_display_resulation
                battery = prod.battery
                operating_system = prod.operating_system
                description = prod.description
                color = prod.color
                warrenty = prod.warrenty
                insurance = prod.insurance
                ports_and_connectivity = prod.ports_and_connectivity
                
                # Create and save Filtered instance
                filtered_instance = FilteredItti(
                title=title,
                brand=brand,
                image=image,
                price = price,
                pprice = pprice,
                link = link,
                model = model,
                processor = processor,
                processor_info = processor_info,
                processor_type = processor_type,
                generation = generation,
                ramm = ramm,
                ram = ram, 
                ram_type = ram_type,
                ram_speed = ram_speed,
                graphics_info = graphics_info,
                graphics = graphics,
                graphics_type = graphics_type,
                sstorage = sstorage,
                storage = storage,
                storage_type = storage_type,
                display = display,
                display_size = display_size,
                touchscreen = touchscreen,
                maximum_display_resulation = maximum_display_resulation,
                battery = battery,
                operating_system = operating_system,
                description = description,
                color = color,
                warrenty = warrenty,
                insurance = insurance,
                ports_and_connectivity = ports_and_connectivity

            )
                
                filtered_instance.full_clean()  # Validate the instance
                filtered_instance.save()
                
            except ValidationError as ve:
                # Handle validation errors
                print(f"Validation Error: {ve}")
                
            except Exception as e:
                # Generic error handling
                print(f"An error occurred: {e}")


def extract_model(title):
    pattern = r"\b(Dell\s+)?(\w+)\s+((?:\d+\s+)?\d+)"
    search_result = re.search(pattern, title)
    if search_result:
        extracted_info = f"{search_result.group(2)} {search_result.group(3)}"
        return extracted_info
    else:
        return "-"

def extract_second_word(title):
    words = title.split(" ")
    if len(words) >= 2:
        return words[1]
    else:
        return "-"



def extractBrand(title):
    pattern = r'^([^ ]+)'
    match = re.search(pattern, title)
    if match:
        brand = match.group(1)
        return brand
    else:
        return "-"


def extract_price(price_range):
    if price_range is None or not isinstance(price_range, str):
        raise ValueError("Invalid input: Not a string or None value")
        
    price_range = price_range.replace(",", "").strip()
    numbers = re.findall(r"\d+\.\d+|\d+", price_range)
    
    if not numbers:
        raise ValueError("Invalid input: No numbers found")
        
    prices = [float(num) for num in numbers]  # Using float to handle decimal points
    
    if len(prices) > 1:
        return min(prices)
    else:
        return prices[0]



def extract_processor_info(title, processor=""):
    # Combine the title and processor strings
    combined_info = title + " " + processor
    intel_core_match = re.search(r'(i[3579])\s*-?\s*(\d{4,5}[A-Za-z]*)', combined_info)
    intel_celeron_match = re.search(r'Celeron', combined_info)
    amd_match = re.search(r'Ryzen (\d+)\s*-?\s*(\d{4}[A-Za-z]*)?', combined_info)
    
    if intel_core_match:
        return f"{intel_core_match.group(1)}-{intel_core_match.group(2)}"
    elif intel_celeron_match:
        return intel_celeron_match.group()
    elif amd_match:
        ryzen_series = amd_match.group(1)
        ryzen_model = amd_match.group(2) if amd_match.group(2) else ""
        return f"Ryzen {ryzen_series} {ryzen_model}".strip()
    else:
        return "-"


def extract_processor_type(title):
    keywords = ["i3", "i5", "i7", "i9", "I3", "I5", "I7", "I9", "AMD", "Amd", "amd", "Celeron", "CELERON", "celeron"]
    p_type_match = re.search(r'\b(?:' + '|'.join(keywords) + r')\b', title)
    if p_type_match:
        return p_type_match.group()
    else:
        return None


def extract_generation(title, processor):
    # Concatenate title and processor info into a single string
    combined_info = title + " " + processor
    
    # Modified regular expression pattern to capture processor numbers
    # Allow optional spaces around either a space or a dash between i\d and the processor number
    pattern = r'(?:Core[\s™]*)?i\d\s*[-\s]\s*(\d+)'
    
    # Check if the title does not contain "amd", "AMD", or "Amd"
    if not re.search(r'\b(?:amd|AMD|Amd)\b', title, re.IGNORECASE):
        match = re.search(pattern, combined_info)
        if match:
            processor_number = match.group(1)  # Capture the processor number
            return processor_number[:2]  # Return the first two digits
    return "-"
        

def extract_ram(title, ram):
    combined_info = title + " " + ram
    pattern = re.compile(r'(\d+GB RAM|\d+GB)', re.IGNORECASE)
    match = pattern.search(combined_info)
    if match:
        return match.group(1).replace(" RAM", "").replace(" ram", "")  # Remove 'RAM' if it exists
    else:
        return "-"

def extract_ram_type(ram):
    pattern = r'\b(ddr[1-5])\b'
    ram_types = re.findall(pattern, ram, re.IGNORECASE)
    
    if ram_types:
        return ram_types[0]
    else:
        return "-"
    
    
def extract_ram_speed(ram):
    pattern = r'(\d+MHz)'
    match = re.search(pattern, ram)
    if match:
        value = match.group(1)
    else:
        value = "-"
    return value


def clean_name(name):
    # Remove certain words from the name
    cleaned = re.sub(r'\d+GB|GDDR\d+|Dedicated Graphics', '', name)
    return cleaned.strip()


def extract_graphics_info(text):
    # Define a regular expression pattern to match the graphics card names.
    # Use non-capturing groups with (?:...) so that only full matches are returned
    pattern = r'(?:AMD[\s\®\™]*Radeon[\s\®\™RX\dMSTVega]*[\s\w\™\®]+)|(?:Intel[\s\®\(\)R]*[Iris\s\(\)R\®Xe\®UHD\s\(\)R]*[\s\wG\d\®]+)|(?:NVIDIA[\s\®]*[GeForce\s\®Quadro\s\®RTX\s\®MX\s\®]*[\w\d\s\-Max\-QTIADA]+)|(?:Qualcomm[\s\®]*Adreno[\s\®]*\d+)'
    
    # Use re.findall to find all instances that match the pattern
    matches = re.findall(pattern, text, re.IGNORECASE)
    clean_matches = [clean_name(match.strip()) for match in matches]
    
    # Clean up matches by stripping extra spaces
    if clean_matches:
        return clean_matches[0]
    else:
        return "-"

def extract_graphics_type(graphics):
    keywords = re.findall(r'\b(?:NVIDIA|INTEL|Intel|AMD|Amd|amd|Nvidia|nvidia|radeon|Radeon|RADEON)\b', graphics)
    if keywords:
        return keywords[0]
    else:
        return "-"


def extracted_storage(storage):
    capacity = re.search(r'(\d+)\s*(TB|Gb|GB|tb|gb)', storage)
    if capacity:
        extracted_capacity = capacity.group(1) + capacity.group(2).upper()
    else:
        extracted_capacity = "-"

    return extracted_capacity


def extract_storage_type(storage):
    keywords = re.findall(r'\b(?:SSD|Solid State Drive|Hard disk|hard disk|Up to 1TB)\b', storage, re.IGNORECASE)
    
    if 'Solid State Drive' in keywords or 'SSD' in keywords:
        return "SSD"
    elif 'Up to 1TB' in keywords:
        return "Hard Disk"
    elif any(['Hard disk' in kw or 'hard disk' in kw for kw in keywords]):
        return "Hard Disk"
    else:
        return "-"


def extract_display_size(display):
    pattern = r'(\d+(?:\.\d+)?)\s*(?:′|″|"|inch|inches|in)'
    size_match = re.search(pattern, display)
    
    if size_match:
        return size_match.group(1)
    else:
        return "-"
    

def extract_touchscreen(display):
    if display.lower() == "yes":
        return "Yes"
    else:
        return "No"



# using pandas

def filter_products(request):
    queryset = Filtered.objects.all()
    data = list(queryset.values())
    df = pd.DataFrame(data)

    # Convert 'price' column to float
    df['price'] = df['price'].astype('float64')

    filter_columns = [
        "brand",
        "model",
        "price",
        "processor",
        "processor_type",
        "generation",
        "ram",
        "graphics_type",
        "storage",
        "storage_type",
        "display_size",
        "touchscreen"
    ]

    filters = {
        "brand": "Brand Name",
        "model": "Model Name",
        "price": "Desired Price Range",
        "processor": "Desired Processor",
        "processor_type": "Desired Processor Type",
        "generation": "Desired Generation",
        "ram": "Desired RAM",
        "graphics_type": "Desired Graphics Type",
        "storage": "Desired Storage",
        "storage_type": "Desired Storage Type",
        "display_size": "Desired Display Size",
        "touchscreen": "Desired Touchscreen"
    }

    filtered_data = df.copy()  # Create a copy of the DataFrame to apply filters

    for column in filter_columns:
        filter_value = request.GET.get(column)  # Get the filter value from the request
        if filter_value:
            if column == 'price':
                # Handle price specially
                if filter_value == "<50000":
                    filtered_data = filtered_data[filtered_data['price'] < 50000]
                elif filter_value == "50000-70000":
                    filtered_data = filtered_data[(filtered_data['price'] >= 50000) & (filtered_data['price'] <= 70000)]
                elif filter_value == "70001-90000":
                    filtered_data = filtered_data[(filtered_data['price'] >= 70001) & (filtered_data['price'] <= 90000)]
                elif filter_value == "90001-120000":
                    filtered_data = filtered_data[(filtered_data['price'] >= 90001) & (filtered_data['price'] <= 120000)]
                elif filter_value == "120001-150000":
                    filtered_data = filtered_data[(filtered_data['price'] >= 120001) & (filtered_data['price'] <= 150000)]
                elif filter_value == ">150000":
                    filtered_data = filtered_data[filtered_data['price'] >= 150000]
                
                # Add more conditions here as needed
            else:
                filtered_data = filtered_data[filtered_data[column].str.contains(filter_value, case=False)]
    context = {
        "filtered_data": filtered_data.to_dict(orient="records"),
    }

    return render(request, "filtered_products.html", context) 

def rankProcessor(x):
    processors = {
    'i3-N305': 1,
    'i5-8269U': 2,
    'i3-1215U': 3,
    'Ryzen 3 3100': 4,
    'Ryzen 3 3300X': 5,
    'Ryzen 3-3250U': 6,
    'Ryzen 3-3250U': 6,
    'i5-7500': 7,
    'i3-1115G': 9,
    'i3-1125G': 10,
    'Ryzen 3 7320U': 11,
    'i3-10100F': 12,
    'i3-10100': 13,
    'Ryzen 3 5300U': 14,
    'i3-10320': 16,
    'i3-9100F': 15,
    'i3-1305U': 17,
    'i5-1240P': 18,
    'i5-8305G': 19,
    'i5-8300H': 20,
    'i7-8557U': 21,
    'i7-6870HQ': 22,
    'i5-1235U': 23,
    'i5-1135G': 24,
    'Ryzen 5 5625U': 25,
    'i5-12500H': 26,
    'i5-2400G': 27,
    'Ryzen 5 1500X': 28,
    'Ryzen 5 1600': 29,
    'i5-1035G': 30,
    'i7-6970HQ': 31,
    'i7-4930MX': 32,
    'i5-1245U': 33,
    'i5-10210U': 34,
    'i7-5950HQ': 35,
    'i7-6920HQ': 36,
    'i7-7820HK': 37,
    
    'i7-7700HQ': 38,
    'i7-6870HQ': 39,
    
    'i5-11400H': 41,
    'i5-12450H': 42,
    'i7-10510U': 43,
    'i5-13420H': 44,
    'i7-4940MX': 45,
    'i7-8557U': 46,
    'Ryzen 5 2600X': 47,
    'Ryzen 5 2600': 48,
    'i7-4790S': 49,
    'i7-4770K': 50,
    'i7-5775C': 51,
    'i7-8559U': 52,
    'i5-7600K': 53,
    'i7-7700T': 54,
    'i5-8400H': 55,
    'i7-4790': 56,
    'i5-9300H': 57,
    'i5-9300HF': 58,
    'i7-7920HQ': 59,
    'Ryzen 5 5500U': 60,
    'i5-11260': 61,
    'i7-8705G': 62,
    'i7-8706G': 63,
    'i7-8709G': 64,
    'i7-6700': 65,
    
    'i7-7820HQ': 66,
    'i5-10200H': 67,
    'Ryzen 5-7535H': 68,
    'Ryzen 5 4600HS': 69,
    'i5-9400H': 70,
    'i5-8500T': 71,
    'i7-4790K': 72,
    'i7-8809G': 73,
    'Ryzen 5 4500U': 74,
    'i5-10300H': 75,
    'i5-1135G7': 76,
    'i7-3960X': 77,
    'i7-6700K': 78,
    'i5-1145G7': 79,
    'i7-7700': 80,
    'i7-4960X': 81,
    'i5-8400': 82,
    'i7-1065G': 83,
    'i5-10400H': 84,
    'i5-10500H': 85,
    'i5-11300H': 86,
    'Ryzen 5 5625': 87,
    'i5-11320H': 88,
    'Ryzen 5 PRO 4650U': 89,
    'Ryzen 5 4600U': 90,
    'i5-12550H': 91,
    'Ryzen 5 4680U': 93,
    'Ryzen 5 PRO 5650U': 94,
    'Ryzen 5 5600U': 95,
    'Ryzen 5 7520U': 96,
    'Ryzen 5 7530U': 97,
    'Ryzen 5 5600H': 98,
    'Ryzen 5 6600H': 107,
    'i5-1155G7': 100,
    'Ryzen 5 PRO 6650U': 101,
    'Ryzen 7 1700': 102,
    'i7-1180G7': 103,
    'Ryzen 7 5825U': 104,
    'i7-5960X': 105,
    'i7-1068G7': 106,
    'Ryzen 5 6600H': 107,
    'i7-1260P': 108,
    'i7-10710U': 109,
    'i7-10810U': 110,
    'i7-1165G7': 111,
    'Ryzen 7 4700U': 112,
    'Ryzen 7 580': 113,
    'i7-8750H': 114,
    'i5-8500': 115,
    'i7-7700K': 116,
    'i5-8600K': 117,
    'Ryzen 7 2700': 118,
    'i7-7740X': 119,
    'i7-1185G7': 120,
    'i7-11370H': 121,
    'i7-8850H': 122,
    'Ryzen 7 5700U': 123,
    'i7-1195G7': 124,
    'i5-11400H': 125,
    'i5-11500H': 126,
    'i7-1280P': 127,
    'i7-1360P': 128,
    'i7-12650H': 129,
    'Xeon E-2176M': 130,
    'i7-10750H': 131,
    'Ryzen 5 5600HS': 132,
    'Ryzen 5 5600H': 132,

    'Ryzen 7 PRO 4750U': 133,
    
    'i7-8700': 134,
    'W-10855M': 135,
    'E5-2697': 136,
    'Ryzen 5 4600H': 137,
    'E5-2680': 138,
    'i5-11260H': 139,
    'Ryzen 7 5700U': 140,
    'Ryzen 7 1700X': 141,
    'Ryzen 7 4800U': 142,
    'i7-11375H': 143,
    'i7-11390H': 144,
    'W-11855M': 145,
    'W-2245': 146,
    'E-2288G': 147,
    'Ryzen 7 4800H': 148,
    'Ryzen 7 1800X': 149,
    'Ryzen 7 PRO 6850U': 150,
    'Ryzen 7 7730U': 151,
    'W-2145': 152,
    'E-2176G': 153,
    'E-2276M': 154,
    'E-2186M': 155,
    'i7-9750H': 156,
    'i7-9850H': 157,
    'i9-9900T': 158,
    'i5-9600K': 159,
    'i7-10850H': 160,
    'i7-1255U': 161,
    'i7-11370H': 162,
    'i7-11390H': 163,
    'Ryzen 7 5700U': 164,
    'Ryzen 7 PRO 6850H': 165,
    'Ryzen 7 6800H': 167,
    'Ryzen 7 7735HS': 168,
    'i9-8950HK': 169,
    'i7-9700': 170,
    'i7-11800H': 160,
    'i7-6950X': 171,
    'i5-11400F': 172,
    'Ryzen 7 2700X': 173,
    'i7-8700K': 174,
    'i7-1250U': 175,
    'i7-8086K': 176,
    'i7-9700K': 177,
    'i7-1185G': 178,
    'Ryzen 7 5800H': 179,
    'W-2185': 180,
    'W-3275': 181,
    'W-2265': 182,
    'W-3245': 182,
    'W-2133': 182,
    'W-2150': 183,
    'W-2155': 184,
    'W-2123': 185,
    'W-2125': 186,
    'W-2140B': 187,
    'W-2102': 188,
    'W-2104': 189,
    'W-2130': 190,
    'W-2135': 191,
    'i7-12700H': 192,
    'Ryzen 7 5825': 193,
    'Ryzen 7 5800H': 194,
    'Ryzen 7 7840H': 195,
    'i9-9940X': 196,
    'i7-10870H': 197,
    'i7-1260P': 198,
    'i9-9880H': 199,
    'i7-1355U': 200,
    'i7-13700H': 201,
    'i9-10980XE': 202,
    'Ryzen 9 3900X': 203,
    'i9-10940X': 204,
    'Ryzen 9 5900X': 205,
    'Ryzen 9 5950X': 206,
    'W-2295': 207,
    'W-3175X': 208,
    'W-3245M': 209,
    'W-3335': 210,
    'E5-2690': 211,
    'E5-2699': 212,
    'E5-2667': 213,
    'E5-2687W': 214,
    'i9-10920X': 215,
    'i9-7900X': 216,
    'i9-7920X': 217,
    'i9-7940X': 218,
    'i9-7960X': 219,
    'i9-7980XE': 220,
    'i9-9980XE': 221,
    'Ryzen 9 3950X': 222,
    'i9-8950H': 223,
    'i9-10980HK': 224,
    'i9-9980HK': 225,
    'i9-10885H': 226,
    'i9-9900K': 227,
    'i9-10850K': 228,
    'i9-9900KS': 229,
    'i9-10900': 230,
    'i9-11900': 231,
    'Ryzen 9 3900XT': 232,
    'Ryzen 9 3950XT': 233,
    'Ryzen 9 4900HS': 234,
    'Ryzen 9 5900HS': 235,
    'i9-10900K': 236,
    'i9-11900K': 237,
    'i9-11950H': 238,
    'i9-12900': 239,
    'i9-12900K': 240,
    'Ryzen 9 4900H': 241,
    'Ryzen 9 5900HS': 242,
    'Ryzen 9 5900': 243,

}
    return processors.get(x, 0)

def compareProcessor1(x,y):
    if x>y:
        return "Performance"
    else:
        return ""
def compareProcessor2(x,y):
    if x<y:
        return "Performance"
    else:
        return ""
def compareProcessor3(x,y):
    if x==y:
        return "Performance"
    else:
        return ""

def rankGpu(x):
    simplified_x = x.replace(" ", "").replace("-", "").replace("®", "").replace("™", "").lower()
    gpu = {
    'Intel UHD Graphics': 1,
    'Intel UHD':1,
    'Intel® UHD Graphics':1,
    'Intel UHD Graphics (Integrated)': 2,
    'Intel UHD Graphics 600': 3,
    'Intel UHD Graphics 605': 4,
    'Intel UHD Graphics G1': 5,
    'Intel UHD Graphics 630': 6,
    'AMD Radeon Graphics Integrated': 7,
    'AMD Radeon graphics (Integrated)': 8,
    'AMD Radeon™ Graphics Integrated':8,
    'Radeon Graphics': 9,
    'AMD Radeon 610M': 10,
    'AMD Radeon RX Vega 3': 11,
    'AMD Radeon Vega 3 Graphics': 12,
    'AMD Radeon™ Vega 3 Graphics':12,
    'AMD Radeon RX Vega 6': 13,
    'AMD Radeon RX Vega 7': 14,
    'Intel Iris Plus Graphics G7': 15,
    'Intel Iris Xe Graphics': 16,
    'Intel(R) Iris(R) Xe Graphics':16,
    'Intel Iris Xe Graphics G4': 17,
    'Intel Iris Xe Max': 18,
    'NVIDIA GeForce MX130': 19,
    'NVIDIA MX130': 19,
    'NVIDIA GeForce MX250': 20,
    'NVIDIA MX250': 20,
    'NVIDIA GeForce MX330': 21,
    'NVIDIA MX330': 21,
    'NVIDIA GeForce MX350': 22,
    'NVIDIA MX 350': 22,
    'NVIDIA GeForce MX450': 24,
    'NVIDIA MX450': 24,
    'NVIDIA GeForce MX550': 25,
    'NVIDIA MX550': 25,
    'NVIDIA GeForce MX570': 26,
    'NVIDIA MX570': 26,
    'NVIDIA MX570A': 26,
    'NVIDIA Quadro T500': 27,
    'NVIDIA Quadro T550': 28,
    'NVIDIA Quadro T1000 Max-Q': 29,
    'NVIDIA Quadro T2000 Max-Q': 30,
    'NVIDIA Quadro T2000': 31,
    'NVIDIA Quadro P520': 32,
    'NVIDIA Quadro P620': 33,
    'NVIDIA T600': 34,
    'NVIDIA T1200': 35,
    'AMD Radeon RX 640': 36,
    'AMD Radeon RX 5300M': 37,
    'NVIDIA GeForce GTX 1650': 38,
    'NVIDIA GeForce GTX 1650 Max-Q': 39,
    'NVIDIA GeForce GTX 1650 Ti': 40,
    'NVIDIA GeForce GTX 1650Ti': 40,
    'NVIDIA GeForce GTX 1660 Ti Max-Q': 41,
    'NVIDIA GeForce GTX 1660Ti Max-Q': 41,
    'AMD Radeon RX 6500M': 42,
    'AMD Radeon RX 6600M': 43,
    'AMD Radeon RX 6700M': 44,
    'AMD Radeon RX 6700S': 45,
    'AMD Radeon RX 6850M XT': 46,
    'AMD Radeon RX 7800MXT': 47,
    'AMD Radeon RX 6850MXT': 46,
    'AMD Radeon RX 7800M XT': 47,
    'NVIDIA RTX 3050': 48,
    'NVIDIA RTX 3050TI': 49,
    'NVIDIA RTX 3060': 50,
    'NVIDIA GeForce RTX 3050': 51,
    'NVIDIA GeForce RTX 3050 Ti': 52,
    'NVIDIA GeForce RTX 3050Ti': 52,
    'NVIDIA GeForce RTX 3060': 53,
    'NVIDIA GeForce RTX 3060 with   VRAM':53,
    'NVIDIA GeForce RTX 3070': 54,
    'NVIDIA GeForce RTX 3070 Ti': 55,
    'NVIDIA GeForce RTX 3070Ti': 55,
    'NVIDIA RTX A1000': 56,
    'AMD Radeon 660M': 57,
    'AMD Radeon 680M': 58,
    'AMD Radeon 780M': 59,
    'NVIDIA GeForce RTX 2050': 60,
    'NVIDIA GeForce RTX 2060': 61,
    'NVIDIA GeForce RTX 2070 Max-Q': 62,
    'NVIDIA GeForce RTX 2070Max-Q': 62,
    'NVIDIA GeForce RTX 2080 SUPER Max-Q': 63,
    'NVIDIA GeForce RTX 2080 SUPERMax-Q': 63,
    'NVIDIA RTX 2000 Ada Generation': 64,
    'Intel Arc A350M': 65,
    'Intel Arc A370M': 66,
    'NVIDIA RTX A2000': 67,
    'NVIDIA RTX A3000': 68,
    'Intel Arc A550M': 69,
    'Intel Arc A730M': 70,
    'NVIDIA RTX A5500': 71,
    'NVIDIA GeForce RTX 4060': 72,
    'NVIDIA GeForce RTX 4070': 73,
    'NVIDIA GeForce RTX 4080': 74,
    'NVIDIA GeForce RTX 4090': 75
}
    simplified_gpu = {key.replace(" ", "").replace("-", "").replace("®", "").replace("™", "").lower(): val for key, val in gpu.items()}
    return simplified_gpu.get(simplified_x, 0)

def compareGpu1(x,y):
    if x>y:
        return "GPU performance"
    else:
        return ""
    
def compareGpu2(x,y):
    if x<y:
        return "GPU performance"
    else:
        return ""

def compareGpu3(x,y):
    if x==y:
        return "GPU perfromace"
    else:
        return ""

def compareProcessor1(x,y):
    if x>y:
        return "Performance"
    else:
        return ""
def compareProcessor2(x,y):
    if x<y:
        return "Performance"
    else:
        return ""
def compareProcessor3(x,y):
    if x==y:
        return "Performance"
    else:
        return ""




def compareStorage(x,y):
    storage = {
        '128GB':1,
        '256GB':2,
        '512':3,
        '1TB':4,
        '2TB':5,
    }
    priority1 = storage.get(x, 0)
    priority2 = storage.get(y, 0)

    if priority1 > priority2:
        result = f"Higher Storage"
        return result
    elif priority1 < priority2:
        result = f"Higher Storage"
        return result
    else:
        result = f"Higher Storage"
        return result


def compareDisplay(x,y):
    display = {
        '14':1,
        '14.0':1,
        '15.5':2,
        '15.6':2,
    }
    priority1 = display.get(x, 0)
    priority2 = display.get(y, 0)

    if priority1 > priority2:
        result = f"Bigger Display"
        return result
    elif priority1 < priority2:
        result = f"Bigger Display"
        return result
    else:
        result = f"Bigger Display"
        return result
        
def compareDisk(x,y):
    disk = {
        'Hard Disk':1,
        'SSD':2
    }

    priority1 = disk.get(x, 0)
    priority2 = disk.get(y, 0)

    if priority1 > priority2:
        result = f"Faster Read and Write"
        return result
    elif priority1 < priority2:
        result = f"Faster Read and Write"
        return result
    else:
        result = f"Faster Read and Write"
        return result
    
def comarePrice(x,y):
    if x<y:
        result = f"lower Price"
        return result
    elif x>y:
        result = f"lower Price"
        return result
    else:
        result = f""
        return result
    
def CompareGen(x,y):
    gen = {
        '5':1,
        '6':2,
        '7':3,
        '8':4,
        '9':5,
        '10':6,
        '11':7,
        '12':8,
        '13':9,
        '14':10
    }
    priority1 = gen.get(x, 0)
    priority2 = gen.get(y, 0)

    if priority1 > priority2:
        result = f"New Processor"
        return result
    elif priority1 < priority2:
        result = f"New Processor"
        return result
    else:
        result = f""
        return result


def rankRam(x):
    # Normalize the input string
    normalized_x = x.replace(" ", "").upper()
    
    ram = {
        '1GB': 1,
        '2GB': 2,
        '3GB': 3,
        '4GB': 4,
        '6GB': 5,
        '8GB': 6,
        '10GB': 7,
        '12GB': 8,
        '16GB': 9,
        '24GB': 10,
        '32GB': 11,
    }
    
    return ram.get(normalized_x, 0)


def compareRam1(x,y):
    if x>y:
        return "Speed"
    else:
        return ""
    
def compareRam2(x,y):
    if x<y:
        return "Speed"
    else:
        return ""
    
def compareRam3(x,y):
    if x==y:
        return "Speed"
    else:
        return ""

# def compareRam1(x,y,z):
#     if x>y or x>z:
#         return "Speed"
#     else:
#         return ""
    
# def compareRam2(x,y,z):
#     if x<y or x<z:
#         return "Speed"
#     else:
#         return ""
    
# def compareRam3(x,y,z):
#     if x==y or x==z:
#         return "Speed"
#     else:
#         return ""
    

def graphics(request):
    filterr = Filtered.objects.all()
    context = {'filterr':filterr}
    return render(request, 'hy.html', context)

def rankStorage(x):
    normalized_x = x.strip().upper()
    
    storage = {
        'HARD DISK': 1,
        'SSD': 2,
    }
    
    return storage.get(normalized_x, 1)

def compareStorage1(x,y):
    if x>y:
        return "Higher Read and Write"
    else:
        return ""
    
def compareStorage2(x,y):
    if x<y:
        return "Higher Read and Write"
    else:
        return ""
    
def compareStorage3(x,y):
    if x==y:
        return "Higher Read and Write"
    else:
        return ""

# def compareStorage1(x,y,z):
#     if x>y or x>z:
#         return "Higher Read and Write"
#     else:
#         return ""
    
# def compareStorage2(x,y,z):
#     if x<y or x<z:
#         return "Higher Read and Write"
#     else:
#         return ""
    
# def compareStorage3(x,y,z):
#     if x==y or x==z:
#         return "Higher Read and Write"
#     else:
#         return ""
    
def rankStorage_info(x):
    normalized_x = x.strip().upper()
    
    storage = {
        '128GB': 1,
        '256GB': 2,
        '512':3,
        '1TB':4,
        '2TB':5,
    }
    
    return storage.get(normalized_x, 1)
