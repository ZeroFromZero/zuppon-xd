c = open('templates/mis_cupones.html', encoding='utf-8').read()
c = c.replace(
    'style="height:50px;margin-right:4px;"',
    'style="height:54px;"'
)
open('templates/mis_cupones.html', 'w', encoding='utf-8').write(c)
print('OK')
