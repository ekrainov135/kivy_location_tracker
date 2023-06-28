from kivy.app import App
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog
from plyer import gps


def open_gps_access_popup():
    dialog = MDDialog(title="GPS Error", text="You need to enable GPS access for the app to function properly")
    dialog.size_hint = [.8, .8]
    dialog.pos_hint = {'center_x': .5, 'center_y': .5}
    dialog.open()


def on_auth_status(general_status, status_message):
    if general_status == 'provider-enabled':
        pass
    else:
        open_gps_access_popup()


def update_blinker_position(*args, **kwargs):
    my_lat = kwargs['lat']
    my_lon = kwargs['lon']
    print("GPS POSITION", my_lat, my_lon)


def get_gps():
    # Request permissions on Android
    if platform == 'android':
        from android.permissions import Permission, request_permissions

        def callback(permission, results):
            if all([res for res in results]):
                print("Got all permissions")
                gps.configure(on_location=update_blinker_position,
                              on_status=on_auth_status)
                gps.start(minTime=1000, minDistance=0)
            else:
                print("Did not get all permissions")

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION], callback)

    # Configure GPS
    if platform == 'ios':
        gps.configure(on_location=update_blinker_position,
                      on_status=on_auth_status)
        gps.start(minTime=1000, minDistance=0)

