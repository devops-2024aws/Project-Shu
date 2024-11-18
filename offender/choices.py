import itertools

gender = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
gender_list = list(set(list(itertools.chain(*gender))))  # this list will be using in templates

health_status = [("Active", "Active"), ("Inactive", "Inactive")]
health_status_list = list(set(list(itertools.chain(*health_status))))  # this list will be using in templates

health_condition = [("Good", "Good"), ("Critical", "Critical"), ("Moderate", "Moderate")]
health_condition_list = list(set(list(itertools.chain(*health_condition))))  # this list will be using in templates
