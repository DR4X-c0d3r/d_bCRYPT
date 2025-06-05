#!/bin/python3

import bcrypt, asyncio, aiofiles, argparse
from time import time
from colorama import Fore

g = Fore.GREEN

r = Fore.RED

RE = Fore.RESET

y = Fore.YELLOW

results = []

attemtps = 0

parser = argparse.ArgumentParser(description='BCRYPT CHECKER!')

parser.add_argument('-p', '--password', help='Required Single Password!', metavar='')
parser.add_argument('-P', '--pass_file', help='Enter A Password List!', metavar='')
parser.add_argument('-L', '--hash_file', help='Enter A Hash List!', required=True, metavar='')

args = parser.parse_args()



async def file_path(path):
	async with aiofiles.open(path, 'r') as lines:
		return [line.strip() for line in await lines.readlines()]

async def checker(password, hashes):

	global attemtps

	try:
		if bcrypt.checkpw(password.encode(), hashes.encode()):
			print(f"{g}Found Match Password: '{RE}{password}{g}' {RE}")
			results.append(hashes + ' : ' + password)

		else:
			print(f"{y}Nothing Found ! [{RE}{attemtps}{y}]{RE}", end='\r', flush=True)

	except Exception as e:
		print(f"{r}Done With This Password '{RE}{password}{r}'{RE}")

	attemtps += 1


async def check_single_pass(password, hashes):
	tasks = []
	async with aiofiles.open(hashes, 'r') as f:
		lines = await f.readlines()
		for line in lines:
			tasks.append(checker(password, line.strip()))
		await asyncio.gather(*tasks)


async def check_list_pass(passwords, hashes):
	tasks = []
	for password in passwords:
		for hashe in hashes:
			tasks.append(checker(password, hashe))
	await asyncio.gather(*tasks)


async def main():
	if args.password:
		await check_single_pass(args.password, args.hash_file)
	else:

		pass_file = await file_path(args.pass_file)

		hash_file = await file_path(args.hash_file)

		await check_list_pass(pass_file, hash_file)

start = time()
asyncio.run(main())
end = time()
print(f"Done in {(end - start):.2f}s")
if results:
	print(f"{g}MATCHES FOUND!:{RE}")
	for result in results:
		print(result)
else:
	print(f"{r}NO MATCHES FOUND!{RE}")
