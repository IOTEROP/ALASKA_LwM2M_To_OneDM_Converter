# LwM2M Objects to OneDM

Provisioning a LwM2M Device into the platform takes optionally a mapping between the LwM2M Objects and the OneDM objects. To help to generate it, the Python script `convert_lwm2m_to_onedm.py` is provided.

Let's say that a LwM2M Device exposes the following objects:

- /1/0
- /3/0
- /3303/0

Using the script, the generated mapping will be:

- /things/DeviceMapping
  - /things/LwM2M_Server
  - /things/Device
  - /things/Temperature

Let's take a concrete example by provisioning a template to Alaska platform. The following base file can be used to provision a template called `MyTemplateTree`.

`base_template.json`:

```json
{
  "operation": "INSERT",
  "templates": [
    {
      "templateId": "MyTemplateTree",
      "name": "MyTemplateTree",
      "mappings": {
        "things": [
        ]
      }
    }
  ]
}
```

Let's now run the Python script with the following options:

```bash
python3 -m pip install -r requirements.txt # Install the script's dependencies (to be done the first time)

python3 convert_lwm2m_to_onedm.py -b base_template.json -i 1 3 3303 -o template_provisioning.json
```

As output, it'll create the file `template_provisioning.json` with the content:

```json
{
  "operation": "INSERT",
  "templates": [
    {
      "templateId": "MyTemplateTree",
      "name": "MyTemplateTree",
      "mappings": {
        "things": [
          {
            "id": "DeviceMapping",
            "name": "LwM2M Objects",
            "things": [
              {
                "id": "LwM2M_Server",
                "name": "LwM2M_Server",
                "properties": [
                  {
                    "id": "Short_Server_ID",
                    "name": "Short_Server_ID",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/1/0/0"
                    }
                  },
                  {
                    "id": "Lifetime",
                    "name": "Lifetime",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/1/0/1"
                    }
                  },
                  {
                    "id": "Default_Minimum_Period",
                    "name": "Default_Minimum_Period",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/1/0/2"
                    }
                  },
                  {
                    "id": "Default_Maximum_Period",
                    "name": "Default_Maximum_Period",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/1/0/3"
                    }
                  },
                  {
                    "id": "Disable_Timeout",
                    "name": "Disable_Timeout",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/1/0/5"
                    }
                  },
                  {
                    "id": "Notification_Storing_When_Disabled_or_Offline",
                    "name": "Notification_Storing_When_Disabled_or_Offline",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/1/0/6"
                    }
                  },
                  {
                    "id": "Binding",
                    "name": "Binding",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/1/0/7"
                    }
                  }
                ],
                "actions": [
                  {
                    "id": "Disable",
                    "name": "Disable",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/1/0/4",
                      "operation": "LWM2M_EXECUTE",
                      "defaultValue": ""
                    }
                  },
                  {
                    "id": "Registration_Update_Trigger",
                    "name": "Registration_Update_Trigger",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/1/0/8",
                      "operation": "LWM2M_EXECUTE",
                      "defaultValue": ""
                    }
                  }
                ]
              },
              {
                "id": "Device",
                "name": "Device",
                "properties": [
                  {
                    "id": "Manufacturer",
                    "name": "Manufacturer",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/0"
                    }
                  },
                  {
                    "id": "Model_Number",
                    "name": "Model_Number",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/1"
                    }
                  },
                  {
                    "id": "Serial_Number",
                    "name": "Serial_Number",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/2"
                    }
                  },
                  {
                    "id": "Firmware_Version",
                    "name": "Firmware_Version",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/3"
                    }
                  },
                  {
                    "id": "Available_Power_Sources",
                    "name": "Available_Power_Sources",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/6"
                    }
                  },
                  {
                    "id": "Power_Source_Voltage",
                    "name": "Power_Source_Voltage",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/7"
                    }
                  },
                  {
                    "id": "Power_Source_Current",
                    "name": "Power_Source_Current",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/8"
                    }
                  },
                  {
                    "id": "Battery_Level",
                    "name": "Battery_Level",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/9"
                    }
                  },
                  {
                    "id": "Memory_Free",
                    "name": "Memory_Free",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/10"
                    }
                  },
                  {
                    "id": "Error_Code",
                    "name": "Error_Code",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/11"
                    }
                  },
                  {
                    "id": "Current_Time",
                    "name": "Current_Time",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/13"
                    }
                  },
                  {
                    "id": "UTC_Offset",
                    "name": "UTC_Offset",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/14"
                    }
                  },
                  {
                    "id": "Timezone",
                    "name": "Timezone",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/15"
                    }
                  },
                  {
                    "id": "Supported_Binding_and_Modes",
                    "name": "Supported_Binding_and_Modes",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/16"
                    }
                  },
                  {
                    "id": "Device_Type",
                    "name": "Device_Type",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/17"
                    }
                  },
                  {
                    "id": "Hardware_Version",
                    "name": "Hardware_Version",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/18"
                    }
                  },
                  {
                    "id": "Software_Version",
                    "name": "Software_Version",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/19"
                    }
                  },
                  {
                    "id": "Battery_Status",
                    "name": "Battery_Status",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/20"
                    }
                  },
                  {
                    "id": "Memory_Total",
                    "name": "Memory_Total",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/21"
                    }
                  },
                  {
                    "id": "ExtDevInfo",
                    "name": "ExtDevInfo",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/22"
                    }
                  }
                ],
                "actions": [
                  {
                    "id": "Reboot",
                    "name": "Reboot",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/4",
                      "operation": "LWM2M_EXECUTE",
                      "defaultValue": ""
                    }
                  },
                  {
                    "id": "Factory_Reset",
                    "name": "Factory_Reset",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/5",
                      "operation": "LWM2M_EXECUTE",
                      "defaultValue": ""
                    }
                  },
                  {
                    "id": "Reset_Error_Code",
                    "name": "Reset_Error_Code",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3/0/12",
                      "operation": "LWM2M_EXECUTE",
                      "defaultValue": ""
                    }
                  }
                ]
              },
              {
                "id": "Temperature",
                "name": "Temperature",
                "properties": [
                  {
                    "id": "Sensor_Value",
                    "name": "Sensor_Value",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3303/0/5700"
                    }
                  },
                  {
                    "id": "Min_Measured_Value",
                    "name": "Min_Measured_Value",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3303/0/5601"
                    }
                  },
                  {
                    "id": "Max_Measured_Value",
                    "name": "Max_Measured_Value",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3303/0/5602"
                    }
                  },
                  {
                    "id": "Min_Range_Value",
                    "name": "Min_Range_Value",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3303/0/5603"
                    }
                  },
                  {
                    "id": "Max_Range_Value",
                    "name": "Max_Range_Value",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3303/0/5604"
                    }
                  },
                  {
                    "id": "Sensor_Units",
                    "name": "Sensor_Units",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3303/0/5701"
                    }
                  }
                ],
                "actions": [
                  {
                    "id": "Reset_Min_and_Max_Measured_Values",
                    "name": "Reset_Min_and_Max_Measured_Values",
                    "mapping": {
                      "protocol": "LWM2M",
                      "protocolPath": "/3303/0/5605",
                      "operation": "LWM2M_EXECUTE",
                      "defaultValue": ""
                    }
                  }
                ]
              }
            ]
          }
        ]
      }
    }
  ]
}
```

The only required argument is `-i`. To see the complete list of the arguments, you can use `-h` option. 

If you don't provide `-o`, the content will be printed in the console. 

If you don't provide `-b`, the script will generate the value of the key `things` only (in the provisioning payload).

If your devices exposes multiple instances of the same object, you can add them by adding multiple times the same Object ID as: `-i 1 3 3303 3303`.
