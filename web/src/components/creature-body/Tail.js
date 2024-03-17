import {MarchingCubes, MarchingCube, Environment, Bounds, CameraControls} from '@react-three/drei';

const RESOLUTION = 4;
export const Tail = ({length}) => {
    return (
        new Array(RESOLUTION).fill(0).map((_, i) => {
            return <MarchingCube
                strength={1}
                subtract={2}
                color={"#f00"}
                position={[length / 2 + i / RESOLUTION * 2 - 1, 0, 0]}
                scale={[length / RESOLUTION, 1 - i / RESOLUTION, 1 - i / RESOLUTION]}
            />;
        })
    );
};