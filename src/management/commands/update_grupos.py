from django.core.management.base import BaseCommand, CommandError
from ... import models

import requests
import xml.etree.ElementTree as ET


class Command(BaseCommand):
	help = "Update the list of GrupoAtendimento from the XML file"
	url = "https://selecoes.lais.huol.ufrn.br/media/grupos_atendimento.xml"

	def handle(self, *args, **options):
		# Get the XML file
		response = requests.get(self.url)
		response.raise_for_status()

		# Parse the XML file
		xml = response.content
		tree = ET.fromstring(xml)

		# Get the list of Estabelecimento
		grupos = tree.findall('grupoatendimento')

		# Clear the table
		models.GrupoAtendimento.objects.all().delete()

		# Create a list of Estabelecimento objects
		bulk = []
		for it in grupos:
			grupo_obj = models.GrupoAtendimento(
				nome = it.find('nome').text)
			bulk.append(grupo_obj)

		# Save the list of Estabelecimento objects
		models.GrupoAtendimento.objects.bulk_create(bulk)