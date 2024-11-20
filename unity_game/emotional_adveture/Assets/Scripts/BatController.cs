using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BatController : MonoBehaviour
{
    private GameManager gameManager;
    private GameObject player;
    private bool nextToPlayer;
    private Rigidbody2D rb2d;
    private SpriteRenderer sr;
    private bool attackReady = true;
    private bool attackRange = false;

    public float followDistance = 5f;
    public float minDistance = 0.5f;
    public float speed = 3f;

    // Start is called before the first frame update
    void Start()
    {
        gameManager = GameManager.instance;
        player = gameManager.player;
        rb2d = GetComponent<Rigidbody2D>();
        sr = GetComponent<SpriteRenderer>();
    }

    // Update is called once per frame
    void Update()
    {
        if (player.GetComponent<PlayerController>().isAlive)
        {
            SearchAndFollow();
            Attack();
        }
    }

    void SearchAndFollow()
    {
        Vector3 playerHead = player.transform.position;
        playerHead.y += 0.8f;

        float distance = Vector3.Distance(playerHead, transform.position);
        nextToPlayer =  distance < followDistance && distance > minDistance;

        if (nextToPlayer)
        {
            followDistance = 8f;

            sr.flipX = (playerHead.x - transform.position.x) > 0;

            transform.position = Vector3.MoveTowards(
                transform.position,
                playerHead,
                speed * Time.deltaTime
            );
        }
        else
        {
            followDistance = 5f;
        }
    }

    void OnTriggerEnter2D(Collider2D col)
    {
        if (col.gameObject.name == "Player")
        {
            attackRange = true;
        }
    }

    void OnTriggerExit2D(Collider2D col)
    {
        if (col.gameObject.name == "Player")
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
                gameManager.AttackPlayer(1);
                attackReady = false;
                Invoke("CanAttack", 1);
            }
        }
    }

    void CanAttack()
    {
        attackReady = true;
    }
}
