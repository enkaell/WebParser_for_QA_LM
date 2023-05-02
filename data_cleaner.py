import json
import aiofiles

import asyncio
import os


class AsyncJSONCleaner:
    def __init__(self):
        self.path = os.sep.join([os.getcwd(), "datasets"])
        self.file_list = [filename for filename in os.listdir(self.path) if
                          ".json" in filename and "cleaned" not in filename]
        os.chdir(self.path)
        asyncio.run(self.main())

    async def clean_line(self, file_as_string: str) -> str:
        cleaned_as_string: str = ""
        escaped: bool = False
        for s in file_as_string.readline():
            if escaped:
                escaped = False
                continue
            if s == "\\":
                escaped = True
                continue
            cleaned_as_string += s
        return cleaned_as_string

    async def clean_file(self, filename: str):
        file_as_string = open(filename, "r")
        res = await self.clean_line(file_as_string)
        async with aiofiles.open("cleaned-" + filename, "x") as f:
            await f.write(json.dumps(res))

    async def main(self):
        tasks = []
        for file in self.file_list:
            tasks.append(self.clean_file(file))
        await asyncio.gather(*tasks)
        print(tasks)


cleaner = AsyncJSONCleaner()
