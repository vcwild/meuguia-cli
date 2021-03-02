import fire
from parsel import Selector
from httpx import get


class MeuGuia:
    def categorias(self):
        response = get('https://meuguia.tv/').text

        s = Selector(response)

        return {'categorias': s.css('h2::text').getall()}
    
    def canal(self, channel):
        request = get(f'https://meuguia.tv/programacao/canal/{channel}')

        if request.status_code != 200:
            return f'Canal {channel} não encontrado'
        
        response = request.text
        s = Selector(response)
        
        return {
            'canal': s.css('#canal_header .devicepadding::text').get(),
            'programa': s.css('h2::text').get(), 
            'início': s.css('div.time::text').get(),
            'categoria': s.css('h3::text').get(),
        }

    def categoria(self, category):
        category = str(category)\
            .capitalize()

        request = get(f'https://meuguia.tv/programacao/categoria/{category}')

        if request.status_code != 200:
            return f'Categoria {category} não encontrada'
        
        response = request.text

        s = Selector(response)

        return {'canais': s.css('h2::text').getall()}


if __name__ == '__main__':
    guia = MeuGuia()
    fire.Fire(guia)