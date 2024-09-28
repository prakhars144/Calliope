import os


def get_env_variable(var_name, default_value=None):
    """Fetch the environment variable or return a default value."""
    try:
        # Attempt to get the environment variable
        value = os.getenv(var_name)
        if value is None:
            # If the environment variable isn't set, raise an exception or use a default
            if default_value is not None:
                value = default_value
            else:
                raise ValueError(
                    f"Environment variable {var_name} not found and no default provided."
                )
        return value
    except Exception as e:
        # Handle any exceptions that might occur
        print(f"Error fetching environment variable {var_name}: {e}")
        return default_value
