from roads.models import Segment, Address, Route
from decimal import Decimal, InvalidOperation # GPT Suggestion
from rest_framework import serializers

class SegmentSerializer(serializers.ModelSerializer):
    # map = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, required=False, use_url=True )
    map = serializers.ImageField(max_length=None, allow_empty_file=False)

    class Meta:
        model = Segment
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        # fields = ['route',]
        fields = '__all__'

# --- Suggestions from GPT --#
# class SegmentUploadItemSerializer(serializers.Serializer):
#     """
#     Validates one row in the bulk payload and normalises keys to a consistent schema.
#     Incoming keys are UPPER_SNAKE_CASE to match your current payload.
#     """
#     # Required identifiers
#     SEGMENT_CODE = serializers.CharField(max_length=10)
#     ROUTE = serializers.CharField(max_length=10)

#     # Optional descriptors (defaulted if blank/missing)
#     SEGMENT_NAME = serializers.CharField(max_length=64, required=False, allow_blank=True)
#     STATE = serializers.CharField(max_length=30, required=False, allow_blank=True)
#     INDEX = serializers.CharField(max_length=2, required=False, allow_blank=True)

#     # Coordinates (coerced to Decimal)
#     # Convention here: NORTHINGS = latitude, EASTINGS = longitude
#     NORTHINGS = serializers.CharField()   # start_lat
#     EASTINGS = serializers.CharField()    # start_lng
#     NORTHINGS2 = serializers.CharField()  # end_lat
#     EASTINGS2 = serializers.CharField()   # end_lng

#     # Optional human-readable names for points
#     START_NAME = serializers.CharField(max_length=30, required=False, allow_blank=True)
#     END_NAME = serializers.CharField(max_length=30, required=False, allow_blank=True)

#     def _coerce_decimal(self, value, field_name):
#         try:
#             d = Decimal(str(value))
#         except (InvalidOperation, TypeError, ValueError):
#             raise serializers.ValidationError(
#                 f"'{field_name}' must be a number (got {value!r})."
#             )
#         return d

#     def _validate_lat(self, d, field_name):
#         if d < Decimal("-90") or d > Decimal("90"):
#             raise serializers.ValidationError(
#                 f"'{field_name}' must be between -90 and 90."
#             )

#     def _validate_lng(self, d, field_name):
#         if d < Decimal("-180") or d > Decimal("180"):
#             raise serializers.ValidationError(
#                 f"'{field_name}' must be between -180 and 180."
#             )

#     def validate(self, attrs):
#         # Coerce & range-check coordinates
#         start_lat = self._coerce_decimal(attrs.get("NORTHINGS"), "NORTHINGS")
#         start_lng = self._coerce_decimal(attrs.get("EASTINGS"), "EASTINGS")
#         end_lat   = self._coerce_decimal(attrs.get("NORTHINGS2"), "NORTHINGS2")
#         end_lng   = self._coerce_decimal(attrs.get("EASTINGS2"), "EASTINGS2")

#         self._validate_lat(start_lat, "NORTHINGS")
#         self._validate_lng(start_lng, "EASTINGS")
#         self._validate_lat(end_lat, "NORTHINGS2")
#         self._validate_lng(end_lng, "EASTINGS2")

#         # Defaults for optional text fields
#         name = attrs.get("SEGMENT_NAME") or "NO NAME"
#         state = attrs.get("STATE") or "NO STATE"

#         # Normalise → internal schema used by your view/services layer
#         attrs["_normalised"] = {
#             "code": attrs["SEGMENT_CODE"].strip(),
#             "route_name": attrs["ROUTE"].strip(),
#             "index": (attrs.get("INDEX") or "").strip(),
#             "name": name.strip(),
#             "state": state.strip(),
#             "start_lat": start_lat,
#             "start_lng": start_lng,
#             "end_lat": end_lat,
#             "end_lng": end_lng,
#             "start_name": (attrs.get("START_NAME") or "").strip(),
#             "end_name": (attrs.get("END_NAME") or "").strip(),
#         }
#         return attrs


class SegmentUploadItemSerializer(serializers.Serializer):
    """
    Validates one row and normalises keys to an internal schema.
    """
    # Required identifiers
    SEGMENT_CODE = serializers.CharField(max_length=10)
    ROUTE = serializers.CharField(max_length=10)

    # Optional descriptors
    SEGMENT_NAME = serializers.CharField(max_length=64, required=False, allow_blank=True)
    STATE = serializers.CharField(max_length=30, required=False, allow_blank=True)
    INDEX = serializers.CharField(max_length=2, required=False, allow_blank=True)

    # Coordinates (NORTHINGS=lat, EASTINGS=lng)
    NORTHINGS = serializers.CharField()
    EASTINGS = serializers.CharField()
    NORTHINGS2 = serializers.CharField()
    EASTINGS2 = serializers.CharField()

    START_NAME = serializers.CharField(max_length=30, required=False, allow_blank=True)
    END_NAME = serializers.CharField(max_length=30, required=False, allow_blank=True)

    def _coerce_decimal(self, value, field_name):
        try:
            d = Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            raise serializers.ValidationError(f"'{field_name}' must be a number (got {value!r}).")
        return d

    def _validate_lat(self, d, field_name):
        if d < Decimal("-90") or d > Decimal("90"):
            raise serializers.ValidationError(f"'{field_name}' must be between -90 and 90.")

    def _validate_lng(self, d, field_name):
        if d < Decimal("-180") or d > Decimal("180"):
            raise serializers.ValidationError(f"'{field_name}' must be between -180 and 180.")

    def validate(self, attrs):
        start_lat = self._coerce_decimal(attrs.get("NORTHINGS"), "NORTHINGS")
        start_lng = self._coerce_decimal(attrs.get("EASTINGS"), "EASTINGS")
        end_lat   = self._coerce_decimal(attrs.get("NORTHINGS2"), "NORTHINGS2")
        end_lng   = self._coerce_decimal(attrs.get("EASTINGS2"), "EASTINGS2")

        self._validate_lat(start_lat, "NORTHINGS")
        self._validate_lng(start_lng, "EASTINGS")
        self._validate_lat(end_lat, "NORTHINGS2")
        self._validate_lng(end_lng, "EASTINGS2")

        name = attrs.get("SEGMENT_NAME") or "NO NAME"
        state = attrs.get("STATE") or "NO STATE"

        attrs["_normalised"] = {
            "code": attrs["SEGMENT_CODE"].strip(),
            "route_name": attrs["ROUTE"].strip(),
            "index": (attrs.get("INDEX") or "").strip(),
            "name": name.strip(),
            "state": state.strip(),
            "start_lat": start_lat,
            "start_lng": start_lng,
            "end_lat": end_lat,
            "end_lng": end_lng,
            "start_name": (attrs.get("START_NAME") or "").strip(),
            "end_name": (attrs.get("END_NAME") or "").strip(),
        }
        return attrs

