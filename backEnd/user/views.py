from django.http import HttpResponse
from django.shortcuts import render

from .forms import AddForm


def index(request):
    # 当提交表单时
    if request.method == 'POST':
        # form 包含提交的数据
        form = AddForm(request.POST)
        # 如果提交的数据合法
        if form.is_valid():
            hour = form.cleaned_data['hour']
            minute = form.cleaned_data['minute']
            second = form.cleaned_data['second']

            # return HttpResponse(str(int(hour)*3600 + int(minute)*60 + int(second)))
            return render(request, 'count.html')

    else:
        form = AddForm()

    return render(request, 'user.html', {'form': form})
