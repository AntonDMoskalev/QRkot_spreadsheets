from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def invested(obj_in, model_db, session: AsyncSession):
    """
    The function of investing projects and distributing donations.
    When creating a new donation or project,
    all available funds (donations) or missing funds (for projects)
    are invested or replenished.
    When full_amount = invested_amount is reached, the project or donation is closed.
    """
    models_db = await session.execute(select(model_db).where(model_db.fully_invested == False).order_by(model_db.create_date))  # noqa
    models_db = models_db.scalars().all()
    if models_db:
        obj_in.invested_amount = 0
        for model in models_db:
            remaining_amount = model.full_amount - model.invested_amount
            investment_amount = obj_in.full_amount - obj_in.invested_amount
            if investment_amount == remaining_amount:
                model.close()
                obj_in.close()
                session.add(model)
            elif investment_amount > remaining_amount:
                setattr(obj_in,
                        'invested_amount',
                        obj_in.invested_amount + remaining_amount)
                model.close()
                session.add(model)
            else:
                setattr(model,
                        'invested_amount',
                        model.invested_amount + investment_amount)
                obj_in.close()
                session.add(model)
    session.add(obj_in)
    return obj_in