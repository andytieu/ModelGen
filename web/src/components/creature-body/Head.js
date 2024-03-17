import {MarchingCubes, MarchingCube, Environment, Bounds, CameraControls} from '@react-three/drei';

const RESOLUTION = 4;
export const Head = ({length, strengthScale}) => {
    return (
        <>
            {new Array(RESOLUTION / 2).fill(0).map((_, i) => {
                return <MarchingCube
                    strength={strengthScale}
                    subtract={1}
                    color={"#f00"}
                    position={[-i / RESOLUTION, 0, 0]}
                    scale={[length / RESOLUTION, 1, 1]}
                />;
            })}
            {new Array(RESOLUTION / 2).fill(0).map((_, i) => {
                return <MarchingCube
                    strength={strengthScale / 2}
                    subtract={1}
                    color={"#f00"}
                    position={[-(i + 2) / RESOLUTION, 0, 0]}
                    scale={[length / RESOLUTION, 1, 1]}
                />;
            })}
        </>
    );
};