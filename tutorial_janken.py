import random
hand=['グー','チョキ','パー']

my = input('グー,チョキ,パーを選んでください')
cp = random.choice(hand)

if my == cp:
    print('引き分け')
elif my=='グー':
    if cp=='チョキ':
        print('勝利')
    elif cp=='パー':
        print('負け')
elif my=='チョキ':
    if cp=='パー':
        print('勝利')
    elif cp=='グー':
        print('負け')  
elif my=='パー':
    if cp=='グー':
        print('勝利')
    elif cp=='チョキ':
        print('負け')

