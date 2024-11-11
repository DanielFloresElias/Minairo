from dataclasses import dataclass, field
from typing import List

@dataclass
class Header:
    seq: int
    stamp: float
    frame_id: str

@dataclass
class Point:
    x: float
    y: float
    z: float

@dataclass
class Quaternion:
    x: float
    y: float
    z: float
    w: float

@dataclass
class Pose:
    position: Point
    orientation: Quaternion

@dataclass
class PoseWithCovariance:
    pose: Pose
    covariance: List[float] = field(default_factory=lambda: [0.0] * 36)

@dataclass
class Vector3:
    x: float
    y: float
    z: float

@dataclass
class Twist:
    linear: Vector3
    angular: Vector3

@dataclass
class TwistWithCovariance:
    twist: Twist
    covariance: List[float] = field(default_factory=lambda: [0.0] * 36)

@dataclass
class Odometry:
    header: Header
    child_frame_id: str
    pose: PoseWithCovariance
    twist: TwistWithCovariance
