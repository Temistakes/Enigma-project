class DBManager:
    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory


    async def __aenter__(self):
        self.session = self.session_factory()

        return self


    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()


    async def commit(self):
        await self.session.commit()


    async def rollback(self):
        await self.session.rollback()
