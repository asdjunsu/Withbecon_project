import base64
import datetime
import os
from io import BytesIO
import numpy as np
import PIL.Image
from fastapi import APIRouter,File, Form, UploadFile
from vision.mask import mask_blush,mask_sebum