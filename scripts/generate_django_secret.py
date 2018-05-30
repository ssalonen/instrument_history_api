import string
import random

# Remove quotes causing trouble in Makefile and escaping
remove_chars='`\"\''
puncts = string.punctuation
for c in remove_chars:
    puncts = puncts.replace(c, '')

print(''.join([random.SystemRandom().choice('{}{}{}'.format(
                string.ascii_letters, string.digits,
                puncts))
                    for i in range(50)]))