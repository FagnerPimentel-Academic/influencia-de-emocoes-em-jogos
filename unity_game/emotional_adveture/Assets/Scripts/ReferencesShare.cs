using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName="New References Share", menuName="My Scripts/References Share", order=1)]

public class ReferencesShare : ScriptableObject
{
    // Deve ser uma collection
    public Dictionary<string, bool> states = new Dictionary<string, bool>()
    {
        { "jumpTriggered", false },
        { "doubleJumpTriggered", false },
        { "attackTriggered", false },
        { "isIdle", false },
        { "isWalking", false },
        { "isRunning", false },
        { "isJumping", false },
        { "isFalling", false },
        { "isGrounded", false },
        { "isCrouching", false },
        { "isClimbing", false },
        { "isAttacking", false },
        { "isHit", false }
    };

    public void SetStates(Dictionary<string, bool> states){
        this.states = states;
    }

    public Dictionary<string, bool> GetStates(){
        return states;
    }

}
