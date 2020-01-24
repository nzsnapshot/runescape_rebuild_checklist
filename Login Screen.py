from firebase import firebase

firebase = firebase.FirebaseApplication('https://kotlin-messender.firebaseio.com/users/KknZotJYQJFvNaGNNBQl', None)

result = firebase.get('/KknZotJYQJFvNaGNNBQl/Fuckwit/', '')
print(result)