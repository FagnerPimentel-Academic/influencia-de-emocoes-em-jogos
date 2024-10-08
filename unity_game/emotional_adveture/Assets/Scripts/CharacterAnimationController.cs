using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public class CharacterAnimationController : MonoBehaviour
{
    public ReferencesShare referencesShare;

    private Dictionary<string, bool> characterStates;
    private Animator animator;
    private Rigidbody2D rb2d;
    private SpriteRenderer spRenderer;

    //int Idle, Run, Jump, Fall, DoubleJump, Hit, WallJump;
    private int Idle = Animator.StringToHash("Idle");
    private int Walk = Animator.StringToHash("Walk");
    private int Run = Animator.StringToHash("Run");
    private int Jump = Animator.StringToHash("Jump");
    private int DoubleJump = Animator.StringToHash("Double Jump");
    private int Fall = Animator.StringToHash("Fall");
    private int Hit = Animator.StringToHash("Hit");
    private int Attack = Animator.StringToHash("Attack");
    private int Crouch = Animator.StringToHash("Crouch");
    private int CrouchAttack = Animator.StringToHash("CrouchAttack");

    private float animationDuration;
    private int newAnimation;
    private int currentAnimation;

    private float crouchAttackAnimDuration = 0.083f;
    private float attackAnimDuration = 0.167f;
    private float hitAnimDuration = 0.125f;

    void Awake()
    {
        animator = GetComponent<Animator>();
        rb2d = GetComponent<Rigidbody2D>();
        spRenderer = GetComponent<SpriteRenderer>();
        characterStates = referencesShare.GetStates();
    }

    // Start is called before the first frame update
    void Start()
    {

    }

    void FixedUpdate(){
        
    }

    // Update is called once per frame
    void Update()
    {
        newAnimation = UpdateAnimation();
        
        if (!(newAnimation == currentAnimation))
        {
            animator.CrossFade(newAnimation, 0, 0);
            currentAnimation = newAnimation;
        }
        
    }

    // private void OnCollisionEnter2D(Collision2D collision){
    //     isGrounded = true;
    // }
    // private void OnCollisionExit2D(Collision2D collision){
    //     isGrounded = false;
    // }

    private int UpdateAnimation()
    {
        characterStates = referencesShare.GetStates();
    
        if (Time.time < animationDuration) return currentAnimation;

        // Priorities
        // if (_attacked) return LockState(Attack, _attackAnimTime);
        // if (_player.Crouching) return Crouch;
        // if (_landed) return LockState(Land, _landAnimDuration);

        // if (characterStates["jumpTriggered"]) return Jump;
        // if (doubleJumpTrigged) return LockState(DoubleJump, 0.15f);

        if(characterStates["isHit"]){
            return LockState(Hit, hitAnimDuration);
        }

        if(!characterStates["isGrounded"]){
            if(characterStates["isJumping"]){
                return Jump;
            }

            if(characterStates["isFalling"]){
                return Fall;
            }
        }

        if(characterStates["isCrouching"]){
            if(characterStates["attackTriggered"]){
                return LockState(CrouchAttack, crouchAttackAnimDuration);
            }

            return Crouch;
        }

        if(characterStates["attackTriggered"])
            return LockState(Attack, attackAnimDuration);

        if(characterStates["isRunning"])
            return Run;

        return characterStates["isWalking"] ? Walk : Idle;

        int LockState(int s, float t)
        {
            animationDuration = Time.time + t;
            return s;
        }
    }
}
