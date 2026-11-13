import discord
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='#', intents=intents)

guias_ecologicas = {
    'basura': {
        'titulo': '🗑️ Generar menos basura',
        'palabras_clave': ['basura', 'tirar'],
        'consejos': [
            'Llevá tu propia bolsa cuando vayas a comprar.',
            'Antes de tirar algo, fijate si se puede arreglar o reutilizar.',
        ],
    },
    'plastico': {
        'titulo': '🥤 Usar menos plástico',
        'palabras_clave': ['plastico'],
        'consejos': [
            'Usá una botella reutilizable en lugar de comprar agua.',
            'Pedí tu bebida sin sorbete.',
        ],
    },
    'agua_luz': {
        'titulo': '💧 Ahorrar agua y luz',
        'palabras_clave': ['agua', 'luz', 'electricidad', 'energia'],
        'consejos': [
            'Cerrá la canilla mientras te cepillás los dientes.',
            'Apagá la luz y desenchufá el cargador cuando no los uses.',
        ],
    },
    'residuos': {
        'titulo': '♻️ Separar los residuos',
        'palabras_clave': ['residuo', 'separar', 'clasificar', 'reciclar'],
        'consejos': [
            'Usá dos bolsas: una para restos de comida y otra para envases.',
            'Enjuagá un poco los envases antes de tirarlos.',
        ],
    },
    'contaminacion': {
        'titulo': '🌍 Contaminar menos día a día',
        'palabras_clave': ['contamin'],
        'consejos': [
            'Para trayectos cortos, caminá o andá en bici.',
            'Comprá productos de tu zona y de estación.',
        ],
    },
}

alternativas_ecologicas = {
    'botella': 'una botella reutilizable de metal o vidrio',
    'bolsa': 'una bolsa de tela que puedas llevar siempre',
    'vaso': 'un vaso o taza reutilizable',
    'sorbete': 'un sorbete de metal, o directamente no usarlo',
    'servilleta': 'servilletas de tela que se lavan',
}

preguntas_quizz = [
    {
        'tipo': 'Opción múltiple',
        'pregunta': '¿Cuál de estas acciones ahorra más agua?',
        'opciones': ['Ducharse 5 minutos', 'Darse un baño de inmersión', 'Lavar el auto con manguera'],
        'respuesta': 'a',
        'explicacion': 'Una ducha corta usa mucha menos agua que llenar la bañera.',
    },
    {
        'tipo': 'Opción múltiple',
        'pregunta': '¿Dónde va una botella de plástico limpia?',
        'opciones': ['Con los restos de comida', 'Con los reciclables', 'En cualquier bolsa'],
        'respuesta': 'b',
        'explicacion': 'Los envases limpios van con los reciclables.',
    },
    {
        'tipo': 'Verdadero o falso',
        'pregunta': 'Un cargador enchufado sin el celular no gasta energía.',
        'opciones': ['Verdadero', 'Falso'],
        'respuesta': 'b',
        'explicacion': 'Gasta un poco aunque no esté cargando nada. Conviene desenchufarlo.',
    },
    {
        'tipo': 'Verdadero o falso',
        'pregunta': 'Una bolsa de tela se puede usar cientos de veces.',
        'opciones': ['Verdadero', 'Falso'],
        'respuesta': 'a',
        'explicacion': 'Por eso reemplaza a muchísimas bolsas de plástico.',
    },
]

desafios = [
    'Pasá un día entero sin usar bolsas de plástico.',
    'Lavá los platos con la canilla cerrada mientras los enjabonás.',
    'Separá hoy los residuos en dos bolsas: restos de comida y envases.',
    'Pasá un día sin usar vasos, platos ni cubiertos descartables.',
]

PUNTOS_POR_RESPUESTA = 5
PUNTOS_POR_DESAFIO = 10

puntos_usuarios = {}
pregunta_actual = {}
desafio_actual = {}


def normalizar(texto):
    texto = texto.lower()
    acentos = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
    for con_acento, sin_acento in acentos.items():
        texto = texto.replace(con_acento, sin_acento)
    return texto


def buscar_tema(texto_usuario):
    texto = normalizar(texto_usuario)
    for tema, guia in guias_ecologicas.items():
        for palabra in guia['palabras_clave']:
            if palabra in texto:
                return tema
    return None


def sumar_puntos(usuario_id, cantidad):
    puntos_usuarios[usuario_id] = puntos_usuarios.get(usuario_id, 0) + cantidad
    return puntos_usuarios[usuario_id]


@bot.event
async def on_ready():
    print(f'EcoGuía conectada como {bot.user} 🌱')


@bot.command()
async def ayuda(ctx):
    await ctx.send(
        '🌱 **¡Hola! Soy EcoGuía.** Esto es lo que podés hacer:\n'
        '`#guia tema` → consejos (basura, plástico, agua, luz, residuos, contaminar)\n'
        '`#alternativa objeto` → una opción más ecológica\n'
        '`#quiz` → una pregunta para sumar puntos\n'
        '`#desafio` → un desafío para hacer hoy\n'
        '`#puntos` → cuántos puntos tenés'
    )


@bot.command()
async def guia(ctx, *, tema_pedido=''):
    tema_seleccionado = buscar_tema(tema_pedido)
    if tema_seleccionado is None:
        await ctx.send('No encontré ese tema 🤔 Probá con: basura, plástico, agua, luz, residuos o contaminar.')
        return

    guia_elegida = guias_ecologicas[tema_seleccionado]
    mensaje = f"**{guia_elegida['titulo']}**\n"
    for consejo in guia_elegida['consejos']:
        mensaje += f'✅ {consejo}\n'
    mensaje += 'Elegí uno y probalo esta semana 💪'
    await ctx.send(mensaje)


@bot.command()
async def alternativa(ctx, *, objeto=''):
    texto = normalizar(objeto)
    for nombre, opcion in alternativas_ecologicas.items():
        if nombre in texto:
            await ctx.send(f'🔄 En lugar de eso, podés usar **{opcion}**.')
            return
    await ctx.send('No tengo ese objeto todavía 🤔 Probá con: botella, bolsa, vaso, sorbete o servilleta.')


@bot.command()
async def quiz(ctx):
    pregunta = random.choice(preguntas_quizz)
    pregunta_actual[ctx.author.id] = pregunta

    letras = ['a', 'b', 'c']
    mensaje = f"❓ **{pregunta['tipo']}**\n{pregunta['pregunta']}\n"
    for i in range(len(pregunta['opciones'])):
        mensaje += f"{letras[i]}) {pregunta['opciones'][i]}\n"
    mensaje += 'Respondé con `#responder` y la letra. Ejemplo: `#responder a`'
    await ctx.send(mensaje)


@bot.command()
async def responder(ctx, respuesta_usuario=''):
    if ctx.author.id not in pregunta_actual:
        await ctx.send('Primero pedí una pregunta con `#quiz` 🙂')
        return

    pregunta = pregunta_actual[ctx.author.id]
    del pregunta_actual[ctx.author.id]

    if respuesta_usuario.lower() == pregunta['respuesta']:
        total = sumar_puntos(ctx.author.id, PUNTOS_POR_RESPUESTA)
        await ctx.send(f"🎉 ¡Correcto! +{PUNTOS_POR_RESPUESTA} puntos (tenés {total}).\n{pregunta['explicacion']}")
    else:
        await ctx.send(
            f"Casi 😅 La respuesta era **{pregunta['respuesta']}**.\n"
            f"{pregunta['explicacion']}\n¡Probá otra con `#quiz`!"
        ) 


@bot.command()
async def desafio(ctx):
    desafio_elegido = random.choice(desafios)
    desafio_actual[ctx.author.id] = desafio_elegido
    await ctx.send(f'🏆 **Tu desafío:** {desafio_elegido}\nCuando lo cumplas, escribí `#cumpli`.')


@bot.command()
async def cumpli(ctx):
    if ctx.author.id not in desafio_actual:
        await ctx.send('Todavía no tenés un desafío. Pedí uno con `#desafio` 🙂')
        return

    del desafio_actual[ctx.author.id]
    total = sumar_puntos(ctx.author.id, PUNTOS_POR_DESAFIO)
    await ctx.send(f'🌟 ¡Muy bien! +{PUNTOS_POR_DESAFIO} puntos (tenés {total}). Cada pequeño cambio suma.')


@bot.command()
async def puntos(ctx):
    total = puntos_usuarios.get(ctx.author.id, 0)
    await ctx.send(f'🌱 {ctx.author.name}, tenés **{total}** puntos.')


with open('token.txt', 'r') as f:
    token = f.read().strip()

bot.run(token)
