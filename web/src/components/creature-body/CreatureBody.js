import {MarchingCubes, MarchingCube, Environment, Bounds, CameraControls} from '@react-three/drei';
import { Tail } from './Tail';

export const CreatureBody = ({
    params: [torsoLength, tailFactor, [thighLength, shinLength, footLength]],
}) => {
    return (
        <>
            {/* <MarchingCube
                strength={1}
                subtract={2}
                color={"#f00"}
                position={[0, 0, 0]}
                scale={[torsoLength, 1, 1]}
            /> */}
            <group position={torsoLength / 2}>
                <Tail length={tailFactor * torsoLength} />
            </group>
        </>
    );
};