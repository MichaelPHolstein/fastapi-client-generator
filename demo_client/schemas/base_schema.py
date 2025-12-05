from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    Base class for all generated Pydantic schemas.

    This class is **not** overwritten when running the generator script again. All
    configurations in this BaseSchema will be used by the generated schemas.

    Recommended use:
        - Add shared validation or serialization behavior.
        - Define global Pydantic model configuration.
        - Extend with common helper methods if needed.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
