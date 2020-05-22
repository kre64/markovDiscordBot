
def makeSentences(model, iters, minLength=1):
	sentences = {}
	for i in range(iters): 
		modelGen = model.chain.gen()
		prevPrevWord = "___BEGIN__"
		prevWord = next(modelGen)
		madeSentence = prevWord + " "

		totalScore = 0
		numWords = 1
		for curWord in modelGen:
			madeSentence += curWord + " "
			numWords += 1
			totalScore += model.chain.model[(prevPrevWord, prevWord)][curWord]
			prevPrevWord = prevWord
			prevWord = curWord

		madeSentence = madeSentence.strip()

		# Filter out short responses
		if numWords == 0: continue
		if numWords < minLength: continue
		if madeSentence in sentences: continue

		totalScore += model.chain.model[(prevPrevWord, prevWord)]["___END__"]

		sentences[madeSentence] = totalScore/float(numWords)

	# Get the sentences as (sentence, score) pairs
	sentences = sentences.items()

	# Sort them so the sentences with the highest score appear first
	sentences = sorted(sentences, key=lambda x: -x[1]) #(key=lambda x: -x[1])

	return sentences


