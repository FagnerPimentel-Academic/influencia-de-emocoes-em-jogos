using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WerewolfController : MonoBehaviour
{
    private GameManager gameManager;
    private AnimationController animationController;
    private SpriteRenderer spriteRenderer;
    private GameObject dog;

    private bool attackReady = true;
    private bool attackRange = false;
    private bool nextToDog = false;
    private bool animationLocked = false;

    public float followDistance = 5f;
    public float minDistance = 1f;
    public float speed = 3f;
    private float hDirection = 0f;

    // Start is called before the first frame update
    void Start()
    {
        gameManager = GameManager.instance;
        dog = gameManager.dog;
        spriteRenderer = GetComponent<SpriteRenderer>();
        animationController = GetComponent<AnimationController>();
    }

    // Update is called once per frame
    void Update()
    {
        if (dog.GetComponent<DogController>().isAlive)
        {
            SearchAndFollow();
            Attack();
        }else{
            PlaySmartAnimation("Idle");
        }
    }

    void SearchAndFollow()
    {
        Vector3 dogPos = dog.transform.position;

        float distance = Vector3.Distance(dogPos, transform.position);
        nextToDog = distance < followDistance && distance > minDistance;

        if (nextToDog)
        {
            followDistance = 8f;

            hDirection = (dogPos.x - transform.position.x > 0) ? 1f : -1f;

            // transform.position = Vector2.MoveTowards(
            //     transform.position,
            //     playerHead,
            //     speed * Time.deltaTime
            // );

            if (hDirection == 1f)
            {
                PlaySmartAnimation("Run");
                spriteRenderer.flipX = false;
                transform.position = new Vector2(
                    transform.position.x + speed * Time.deltaTime,
                    transform.position.y
                );
            }
            else if (hDirection == -1f)
            {
                PlaySmartAnimation("Run");
                spriteRenderer.flipX = true;
                transform.position = new Vector2(
                    transform.position.x - speed * Time.deltaTime,
                    transform.position.y
                );
            }
        }
        else
        {
            PlaySmartAnimation("Idle");
            followDistance = 5f;
        }
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.collider.gameObject.name == "Dog")
        {
            attackRange = true;
        }
    }

    private void OnCollisionExit2D(Collision2D collision)
    {
        if (collision.collider.gameObject.name == "Dog")
        {
            attackRange = false;
        }
    }

    void Attack()
    {
        if (attackRange)
        {
            if (attackReady)
            {
                PlaySmartAnimation("Attack");
                gameManager.AttackDog(2);
                attackReady = false;
                Invoke("CanAttack", 1);
            }
        }
    }

    void CanAttack()
    {
        attackReady = true;
    }

    private void PlaySmartAnimation(string animacao)
    {
        if (!animationLocked)
        {
            animationController.PlayAnimation(animacao);

            if (animacao == "Attack")
            {
                animationLocked = true;
                Invoke("UnlockAnimation", 0.400f);
            }
        }
    }

    private void UnlockAnimation()
    {
        animationLocked = false;
    }
}
