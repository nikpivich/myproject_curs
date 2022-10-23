



# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#
#             current_site = get_current_site(request)
#             print(f'{current_site=}')
#
#             # Отправка письма
#             send_email.delay(current_site.domain, user.id, 'registration/email_confirm.html')
#
#             # Удаление через 300 сек\
#             delete_user.apply_async(args=(user.id,), countdown=300)
#
#             return HttpResponse('Пожалуйста, подтвердите вашу регистрацию. На указанную почту было выслано письмо. '
#                                 'Проверьте папку (Спам), если не видите его во входящих.')
#     else:
#         form = SignupForm()
#
#     return render(request, 'registration/sign_up.html', {'form': form})