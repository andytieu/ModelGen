import {MarchingCubes, MarchingCube, Environment, Bounds, CameraControls} from '@react-three/drei';
import { Tail } from './Tail';
import { Torso } from './Torso';
import { Neck } from './Neck';
import { Head } from './Head';

export const CreatureBody = ({
    params: [torsoLength, tailFactor, [thighLength, shinLength, footLength]],
}) => {
    const strengthScale = 0.125;
    const tailLength = tailFactor * torsoLength;
    return (
        <group scale={[strengthScale, strengthScale, strengthScale]}>
            {/* <group position={[0, 0, 0]}>
                <Tail
                    length={tailLength}
                    strengthScale={strengthScale}
                />
            </group> */}

            <Torso
                length={torsoLength}
                strengthScale={strengthScale}
            />

            {/* <group position={[-torsoLength, 0, 0]}>
                <Neck
                    length={tailLength}
                    strengthScale={strengthScale}
                    taper={1/3}
                />
            </group>

            <group position={[-torsoLength - tailLength, 0, 0]}>
                <Head
                    length={torsoLength}
                    strengthScale={strengthScale}
                />
            </group> */}
        </group>
    );
};