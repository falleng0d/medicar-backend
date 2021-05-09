from django.contrib.auth import get_user_model
from django.urls import reverse

# GET /medicos/
SAMPLE_MEDIC_RESPONSE = [
	{
		"id": 1,
		"crm": 3711,
		"nome": "Drauzio Varella",
		"especialidade": {
			"id": 2,
			"nome": "Pediatria"
		}
	},
	{
		"id": 2,
		"crm": 2544,
		"nome": "Gregory House",
		"especialidade": {
			"id": 3,
			"nome": "Cardiologia"
		}
	},
	{
		"id": 3,
		"crm": 3087,
		"nome": "Tony Tony Chopper",
		"especialidade": {
			"id": 2,
			"nome": "Pediatria"
		}
	}
]
# GET /especialidades/
SAMPLE_SPECIALTY_LIST = [
	"Ginecologia",
	"Pediatria",
	"Cardiologia",
	"Clínico Geral",
]
# GET /consultas/
SAMPLE_APPOINTMENT_RESPONSE = [
	{
		"id": 1,
		"dia": "2020-02-05",
		"horario": "12:00",
		"data_agendamento": "2020-02-01T10:45:0-03:00",
		"medico": {
			"id": 2,
			"crm": 2544,
			"nome": "Gregory House",
			"especialidade": {
				"id": 3,
				"nome": "Cardiologia"
			}
		}
	},
	{
		"id": 2,
		"dia": "2020-03-01",
		"horario": "09:00",
		"data_agendamento": "2020-02-01T10:45:0-03:00",
		"medico": {
			"id": 1,
			"crm": 3711,
			"nome": "Drauzio Varella",
			"especialidade": {
				"id": 2,
				"nome": "Pediatria"
			}
		}
	}
]
# GET /agendas/
SAMPLE_SCHEDULE_RESPONSE = [
	{
		"id": 1,
		"medico": {
			"id": 3,
			"crm": 3087,
			"nome": "Tony Tony Chopper",
			"especialidade": {
				"id": 2,
				"nome": "Pediatria"
			}
		},
		"dia": "2020-02-10",
		"horarios": ["14:00", "14:15", "16:00"]
	},
	{
		"id": 2,
		"medico": {
			"id": 2,
			"crm": 2544,
			"nome": "Gregory House",
			"especialidade": {
				"id": 3,
				"nome": "Cardiologia"
			}
		},
		"dia": "2020-02-10",
		"horarios": ["08:00", "08:30", "09:00", "09:30", "14:00"]
	}
]
# POST /consultas/
SAMPLE_POST_APPOINTMENT_RESPONSE = {
	"id": 2,
	"dia": "2020-03-01",
	"horario": "09:00",
	"data_agendamento": "2020-02-01T10:45:0-03:00",
	"medico": {
		"id": 1,
		"crm": 3711,
		"nome": "Drauzio Varella",
		"especialidade": {
			"id": 2,
			"nome": "Pediatria"
		}
	}
}

SAMPLE_SPECIALTY_RESPONSE = [
	{
		"id": 1,
		"nome": "Pediatria"
	},
	{
		"id": 2,
		"nome": "Ginecologia"
	},
	{
		"id": 3,
		"nome": "Cardiologia"
	},
	{
		"id": 4,
		"nome": "Clínico Geral"
	}
]


SPECIALTY_URL = reverse('specialty:specialty-list')
MEDIC_URL = reverse('medic:medic-list')
SCHEDULE_URL = '/agenda/'
APPOINTMENT_URL = '/consultas/'


def sample_user(username='test', password='testpass'):
	"""Create a sample user"""
	return get_user_model().objects.get_or_create(username=username, password=password)[0]
