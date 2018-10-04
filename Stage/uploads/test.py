liste1 = ['stage1', 'stage2', 'stage3', 'stage4', 'stage5']
liste2 = [{'a': 1, 'stage':'stage2'}, {'a':2, 'stage':'stage4'}, {'a':8, 'stage':'stage3'}]
liste3 = ['stage1', 'stage3']

if liste3 in liste1:
	print('ok')
else:
	print('pas ok')