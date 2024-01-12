from django.core.management.base import BaseCommand, CommandError
from ... import models

import requests
import xml.etree.ElementTree as ET


class Command(BaseCommand):
	help = "Update the XML file"
	# I don't know if it should be an argument or just a constant
	url = "https://selecoes.lais.huol.ufrn.br/media/estabelecimentos_pr.xml"


	def handle(self, *args, **options):
		# Get the XML file
		response = requests.get(self.url)
		response.raise_for_status()

		# Parse the XML file
		xml = response.content
		tree = ET.fromstring(xml)

		# Get the list of Estabelecimento
		estabelecimentos = tree.findall('estabelecimento')

		# Clear the table
		models.Estabelecimento.objects.all().delete()

		# Create a list of Estabelecimento objects
		estabelecimentos_obj = []
		for estabelecimento in estabelecimentos:
			estabelecimento_obj = models.Estabelecimento(
				cnes=estabelecimento.find('co_cnes').text,
				razao_social=estabelecimento.find('no_razao_social').text,
				nome_fantasia=estabelecimento.find('no_fantasia').text,
				logadouro=estabelecimento.find('no_logradouro').text,
				endereco=estabelecimento.find('nu_endereco').text,
				bairro=estabelecimento.find('no_bairro').text,
				cep=estabelecimento.find('co_cep').text,
				telefone=estabelecimento.find('nu_telefone').text,
			)
			estabelecimentos_obj.append(estabelecimento_obj)

		# Save the list of Estabelecimento objects
		models.Estabelecimento.objects.bulk_create(estabelecimentos_obj)
