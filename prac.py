import re
full_name = "new!\
squishmallows™ sealife squad 5in\
$4.00"

def get_size(full_name):
    regexp = re.compile(r'in')
    regexp2 = re.compile(r"'")
    for x in full_name.split():
        if regexp.search(x):
            return x
        if regexp2.search(x):
            return x
    return 'N/A'

print(get_size(full_name))
print(full_name.split())