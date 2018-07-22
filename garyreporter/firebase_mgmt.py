from python-firebase.firebase import firebase
firebase = firebase.FirebaseApplication('https://web-search-a5658.firebaseio.com', None)
result = firebase.get('/users/2', None, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
print result
#{'2': 'Jane Doe'}
