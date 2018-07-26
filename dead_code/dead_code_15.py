def qualcosa(n):
	if n==1 :
		return 1
	if n==2 :
		return 1

	return qualcosa(n-1) + qualcosa(n-2)