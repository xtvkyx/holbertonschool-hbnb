def register_routes(rest_api):
    from app.api.v1.users import ns as users_ns
    from app.api.v1.amenities import ns as amenities_ns

    rest_api.add_namespace(users_ns, path="/api/v1/users")
    rest_api.add_namespace(amenities_ns, path="/api/v1/amenities")
