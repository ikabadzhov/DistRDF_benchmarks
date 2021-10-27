
from datetime import datetime

first_start = False
end_t = ''
begin_t = ''
to_print = False


chunks = []
i = 0
chu = []

with open('distrdf_timestamps.out') as f:  # after running the .sh script
	for line in f:
		if line.startswith("python3"):
			chunks.append(chu)
			i +=1
			chu = []

		chu.append(line)

#print(chunks[2][0])

for i in range(1, len(chunks), 1):
	#print(chunks[i][0][:-1])
	begin_t = datetime.strptime(chunks[i][1][33:-1], "%y-%m-%d %H:%M:%S.%f")
	
	end_t = datetime.strptime(chunks[i][-6][31:-1], "%y-%m-%d %H:%M:%S.%f")
	print(chunks[i][-3][:-1])
	print("Timer from Base.py", end_t - begin_t)
	
	#if "=" in str(chunks[i]):
	#	print(i, chunks[i])
	print()
