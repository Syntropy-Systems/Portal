from project.models.users import *
from project.models.orders import *
from project.views.common import *


# Common template
def pagination(request):
	return render(request, 'common/pagination.html')

