from django.shortcuts import render

# Create your views here.
def get_location_info(latitude, longitude):
    nominatim_url = "https://nominatim.openstreetmap.org/reverse"

    params = {
        "format": "json",
        "lat": latitude,
        "lon": longitude,
    }

    response = requests.get(nominatim_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "address" in data:
            address = data["address"]
            municipality = address.get("city", address.get("town", address.get("village", "")))
            suburb = address.get("suburb", "")
            state = address.get("state", "")
            return {
                "municipality": municipality,
                "suburb": suburb,
                "state": state,
            }

    return {}

def dms_to_dd(dms):
    degrees, minutes, seconds = dms
    dd = None
    if degrees:
        dd = float(degrees)
    if minutes:
        dd += float(minutes) / 60
    if seconds:
        dd += float(seconds) / 3600
    return dd

@login_required
def cad_abordagem(request):
    template = 'cadastro_abordagem.html'
    if request.method == 'GET':
        # __lte é igual a menor ou igual a, __gte é igual a maior ou igual a
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(comandante='True')
        try:
            instituicao = ModelUsuarios.objects.get(id=request.user.id).instituicao
        except:
            instituicao = 'NAO DEFINIDO'
        context = {'operacoes':operacoes,
                   'chefes': chefes,
                   'instituicao': instituicao,
                   }
        return render(request, template,context)
    else:
        foto_abordado = request.POST.get('foto_abordado')
        foto_documento = request.POST.get('foto_documento')
        nro_documento = request.POST.get('nro_documento')
        nome_envolvido = request.POST.get('nome_envolvido')
        nome_mae = request.POST.get('nome_mae')
        data_nascimento = request.POST.get('data_nasc')
        comandante = request.POST.get('chefe_guarnicao')
        operacao = request.POST.get('nome_op')
        
        imagem_abordado = foto_abordado
        foto_abordado = re.sub('^data:image/.+;base64,', '', foto_abordado)
        image_data = base64.b64decode(foto_abordado)
        img = Image.open(BytesIO(image_data))
        exif_data = img._getexif()
        print(request.POST.get('locationResult'))
        
        if exif_data and 0x8825 in exif_data:
            gps_info = exif_data[0x8825]
            latitude = dms_to_dd(gps_info.get(2, [None]))
            longitude = dms_to_dd(gps_info.get(4, [None]))
            # Assumir a direção como "N" para latitude e "E" para longitude se não especificada
            if "N" not in gps_info.get(3, ["N"]):
                latitude *= -1
            if "W" in gps_info.get(3, []):
                longitude *= -1
            location_info = get_location_info(latitude, longitude)
            print("Latitude (DD):", latitude)
            print("Longitude (DD):", longitude)
            print("Município:", location_info.get("municipality", "N/A"))
            print("Bairro:", location_info.get("suburb", "N/A"))
            print("Estado:", location_info.get("state", "N/A"))
        
        user_ip = get_client_ip(request)
        location_data = get_location_by_ip(user_ip)
        latitude_ip = location_data['latitude']
        longitude_ip = location_data['longitude']
        print(latitude_ip, ',',longitude_ip, '--')
    usuario = ModelUsuarios.objects.get(id=request.user.id)
    
    print(imagem_abordado[:30])
    operacao = ModelOperacoes.objects.get(id=operacao)
    imagem = ModelImagens(imagem=imagem_abordado)
    imagem.save()
    pessoa = ModelPessoas.objects.get(id_pessoa=nome_envolvido)
    abordagem = ModelRegistrosAbordagem(comandante=comandante,id_usuario=usuario,id_operacao=operacao if operacao else None, id_envolvido=pessoa,id_foto_abordado=imagem)
    
    abordagem.save()

    
    context = {}
    # return HttpResponse('Abordagem cadastrada com sucesso')
    return redirect('registro_acoes')

def get_client_ip(request):
    # Tente obter o IP público do cliente usando um serviço externo
    try:
        external_ip = requests.get('https://ipinfo.io').text.strip()
        return external_ip
    except requests.RequestException:
        pass

    # Caso não seja possível obter o IP público, obtenha o IP local
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location_by_ip(ip):
    url = f"https://ipinfo.io/{ip}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        if 'loc' in data:
            latitude, longitude = data['loc'].split(',')
            return {'latitude': latitude, 'longitude': longitude}
    return {'latitude': 0, 'longitude': 0}

@login_required
def abordagem_veicular(request):
    template = 'cadastro_veiculo.html'
    if request.method == 'GET':
        # __lte é igual a menor ou igual a, __gte é igual a maior ou igual a
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(comandante='True')
        context = {'operacoes':operacoes,
                   'chefes': chefes,
                   }
        return render(request, template,context)
    else:
        tipo_veiculo = request.POST.get('tipo_veiculo')
        placa = request.POST.get('placa')
        nome_proprietario = request.POST.get('proprietario')
        nome_condutor = request.POST.get('condutor')
        irregularidade = request.POST.get('irregularidade')
        veiculo_apreendido = request.POST.get('veiculo_apreendido')
        comandante = request.POST.get('chefe_guarnicao')
        operacao = request.POST.get('nome_op')
    
    usuario = User.objects.get(id=request.user.id)
    
    abordagem = ModelRegistrosAbordagem(comandante=comandante,id_usuario_id=usuario,operacao=operacao if operacao else None,id_tipo_abordagem=2)
    abordagem.save()

    Veiculo = ModelVeiculos(tipo_veiculo=tipo_veiculo,placa=placa,proprietario=nome_proprietario,condutor=nome_condutor,irregularidade=irregularidade,veiculo_apreendido='True' if veiculo_apreendido == 'on' else 'False',id_abordagem=abordagem)
    print(Veiculo)
    Veiculo.save()
    context = {}
    return redirect('indicadores')

@login_required
def fiscalizacao_estabelecimento(request):
    template = 'cadastro_estabelecimento.html'
    if request.method == 'GET':
        # __lte é igual a menor ou igual a, __gte é igual a maior ou igual a
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(comandante='True')
        context = {'operacoes':operacoes,
                   'chefes': chefes,
                   }
        return render(request, template,context)
    else:
        tipo_estabelecimento = request.POST.get('tipo_estabelecimento')
        endereco = request.POST.get('endereco')
        proprietario = request.POST.get('proprietario')
        irregularidade = request.POST.get('irregularidade')
        estabelecimento_interditado = request.POST.get('estabelecimento_interditado')
        comandante = request.POST.get('chefe_guarnicao')
        operacao = request.POST.get('nome_op')
        
    usuario = User.objects.get(id=request.user.id)
    
    abordagem = ModelRegistrosAbordagem(comandante=comandante,id_usuario_id=usuario,operacao=operacao if operacao else None,id_tipo_abordagem=3)
    abordagem.save()

    estabelecimento = ModelEstabelecimentos(tipo_estabelecimento=tipo_estabelecimento,endereco=endereco,proprietario=proprietario,irregularidade=irregularidade,estabelecimento_interditado='True' if estabelecimento_interditado == 'on' else 'False',id_abordagem=abordagem)
    print(estabelecimento)
    estabelecimento.save()
    context = {}
    return HttpResponse('fiscalizacao de estabelecimento cadastrada com sucesso')