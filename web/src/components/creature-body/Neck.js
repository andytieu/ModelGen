import {MarchingCubes, MarchingCube, Environment, Bounds, CameraControls} from '@react-three/drei';

const RESOLUTION = 8;
export const Neck = ({length, taper, strengthScale}) => {
    return (
        new Array(RESOLUTION - 1).fill(0).map((_, i) => {
            return <MarchingCube
                strength={(1 - i / RESOLUTION * taper)**2 * strengthScale}
                subtract={1}
                color={"#0f0"}
                position={[-i / RESOLUTION, 0, 0]}
                scale={[length / RESOLUTION, 1, 1]}
            />;
        })
    );
};