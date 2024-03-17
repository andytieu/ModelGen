import {MarchingCubes, MarchingCube, Environment, Bounds, CameraControls} from '@react-three/drei';

export const Torso = ({length, strengthScale, resolution}) => {
    return (
        new Array(resolution).fill(0).map((_, i) => {
            return <MarchingCube
                strength={strengthScale}
                subtract={3}
                color={"#00f"}
                position={[-i / resolution, 0, 0]}
                scale={[1, 1, 1]}
            />;
        })
    );
}